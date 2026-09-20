"""Generate a fresh SmartThings PAT and deliver it to a configured HA service.

pat_rotator.py is vendored as a git submodule from
https://github.com/pallemannen/SmartThings-PAT-Rotator (a fork of
TryTryAgain/SmartThings-PAT-Rotator with reliability fixes - see that
repo's own history). Its own push_token_to_ha()/main() write to an
input_text helper - we don't use either, we just call run_browser()
directly and deliver the result ourselves via a proper HA service call
instead.
"""
import json
import logging
import os
from pathlib import Path

import requests

log = logging.getLogger("rotate_and_submit")

STATE_FILE = Path(os.environ.get("STATE_FILE", "/data/browser_state.json"))

REAUTH_NOTIFICATION_ID = "smartthings_pat_rotator_reauth"

# These specific error messages (raised by pat_rotator.py's do_login()) only
# happen when Samsung's fraud detection throws a real CAPTCHA/MFA challenge
# instead of proceeding to the password field - confirmed via a debug
# screenshot. This isn't always a permanently dead session though - confirmed
# live, one of these cleared on its own within the hour with no cookie
# reseed - so run.py retries a few times before treating it as one.
REAUTH_ERROR_SIGNATURES = (
    "Could not find email input",
    "Could not find password input",
    "Login may have failed",
)


def is_reauth_required(exc: Exception) -> bool:
    message = str(exc)
    if "chrome-error://" in message:
        # A browser-internal error page (from a network-changed navigation
        # failure landing on chrome-error://chromewebdata/, for example)
        # raises the exact same "Could not find email input" text as a
        # real Samsung CAPTCHA block, but it's a transient, unrelated
        # cause - confirmed live, this misfired the reauth alert for a
        # plain network hiccup. Re-seeding cookies wouldn't have fixed it.
        return False
    return any(sig in message for sig in REAUTH_ERROR_SIGNATURES)


def alert_reauth_needed(exc: Exception) -> None:
    call_ha_service(
        "persistent_notification.create",
        {
            "title": "SmartThings PAT Rotator needs re-authentication",
            "message": (
                "Samsung blocked automated login with a CAPTCHA or MFA "
                "challenge on 3 attempts in a row, an hour apart.\n\n"
                f"Error: {exc}\n\n"
                "To fix: log into account.smartthings.com (and, "
                "recommended, account.samsung.com too) in a real browser, "
                "run `tools/extract_samsung_cookies.py`, and paste its "
                "output into this add-on's `cookies_json` config option, "
                "then restart it."
            ),
            "notification_id": REAUTH_NOTIFICATION_ID,
        },
    )


def dismiss_reauth_alert() -> None:
    # Best-effort cleanup, called right after a successful rotation - must
    # never turn a working rotation into a reported failure just because
    # there was nothing to dismiss.
    try:
        call_ha_service(
            "persistent_notification.dismiss",
            {"notification_id": REAUTH_NOTIFICATION_ID},
        )
    except Exception:
        log.debug("Nothing to dismiss (or dismiss failed) - ignoring", exc_info=True)


def load_options() -> dict:
    with open("/data/options.json") as f:
        return json.load(f)


def call_ha_service(target_service: str, payload: dict) -> None:
    domain, service = target_service.split(".", 1)
    supervisor_token = os.environ["SUPERVISOR_TOKEN"]
    url = f"http://supervisor/core/api/services/{domain}/{service}"
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {supervisor_token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    resp.raise_for_status()


def _cookies_to_storage_state(raw_cookies: list) -> dict:
    """Convert extract_samsung_cookies.py's output into Playwright's
    storage_state format (same shape browser_state.json already uses)."""
    relevant_substrings = ("samsung.com", "smartthings.com")
    cookies = []
    for c in raw_cookies:
        if not any(s in c["domain"] for s in relevant_substrings):
            continue
        expires = c.get("expires")
        expires = float(expires) if expires else -1
        cookies.append(
            {
                "name": c["name"],
                "value": c["value"],
                "domain": c["domain"],
                "path": c.get("path") or "/",
                "expires": expires,
                "httpOnly": bool(c.get("httpOnly", False)),
                "secure": bool(c.get("secure", False)),
                "sameSite": "None" if c.get("secure") else "Lax",
            }
        )
    return {"cookies": cookies, "origins": []}


def _clear_cookies_json_option(options: dict) -> None:
    # /addons/self/options replaces the whole options object, it doesn't
    # merge - sending only the changed field fails schema validation
    # ("Missing option 'samsung_email'..."), confirmed via direct testing.
    supervisor_token = os.environ["SUPERVISOR_TOKEN"]
    resp = requests.post(
        "http://supervisor/addons/self/options",
        headers={
            "Authorization": f"Bearer {supervisor_token}",
            "Content-Type": "application/json",
        },
        json={"options": {**options, "cookies_json": ""}},
        timeout=30,
    )
    resp.raise_for_status()


def maybe_seed_cookies_from_config(options: dict) -> None:
    """If a fresh cookie export was pasted into the cookies_json config
    option, seed it as the browser session and clear the option - both so
    it doesn't sit around in plaintext config, and so we don't try to
    re-seed the same value every cycle."""
    raw = options.get("cookies_json", "").strip()
    if not raw:
        return

    try:
        raw_cookies = json.loads(raw)
    except json.JSONDecodeError as e:
        log.error("cookies_json option is not valid JSON, ignoring: %s", e)
        return

    storage_state = _cookies_to_storage_state(raw_cookies)
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(storage_state, f)
    log.info(
        "Seeded a new browser session from %d cookies pasted via config",
        len(storage_state["cookies"]),
    )

    try:
        _clear_cookies_json_option(options)
    except Exception:
        log.exception(
            "Seeded the session but failed to clear the cookies_json option "
            "- clear it manually so it isn't re-seeded from a stale value "
            "next cycle"
        )


def _set_login_env(options: dict) -> None:
    # pat_rotator.py reads these from the environment at import time.
    # SAMSUNG_EMAIL/PASSWORD are the only ones we actually use (run_browser()/
    # run_keep_alive() only need these). HA_TOKEN is also required at import
    # time even though we never call push_token_to_ha() - it just needs to
    # exist as a string, its value is irrelevant to the code path we
    # actually use.
    os.environ["SAMSUNG_EMAIL"] = options["samsung_email"]
    os.environ["SAMSUNG_PASSWORD"] = options["samsung_password"]
    os.environ.setdefault("HA_TOKEN", "unused")
    if options.get("samsung_totp_secret"):
        os.environ["SAMSUNG_TOTP_SECRET"] = options["samsung_totp_secret"]


async def rotate_once() -> None:
    options = load_options()
    maybe_seed_cookies_from_config(options)
    _set_login_env(options)

    import pat_rotator  # noqa: E402  (must import after env vars are set)

    log.info("Starting PAT rotation via Playwright...")
    token = await pat_rotator.run_browser(debug=False)
    log.info("Got a fresh PAT, delivering to %s", options["target_service"])
    call_ha_service(options["target_service"], {options["token_field"]: token})


async def keep_alive_once() -> bool:
    """Ping the saved session so it doesn't go idle-stale between rotations.

    Only navigates to the tokens page and checks we land there rather than
    on login - never generates a token, so unlike rotate_once() it can run
    far more often without touching PAT expiry at all.
    """
    options = load_options()
    maybe_seed_cookies_from_config(options)
    _set_login_env(options)

    import pat_rotator  # noqa: E402  (must import after env vars are set)

    return await pat_rotator.run_keep_alive()
