"""Generate a fresh SmartThings PAT and deliver it to a configured HA service.

Deliberately does NOT modify pat_rotator.py (vendored unmodified from
https://github.com/TryTryAgain/SmartThings-PAT-Rotator as a git submodule).
Its own push_token_to_ha()/main() write to an input_text helper - we don't
use either, we just call run_browser() directly and deliver the result
ourselves via a proper HA service call instead.
"""
import json
import logging
import os
from pathlib import Path

import requests

log = logging.getLogger("rotate_and_submit")

STATE_FILE = Path(os.environ.get("STATE_FILE", "/data/browser_state.json"))


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


async def rotate_once() -> None:
    options = load_options()
    maybe_seed_cookies_from_config(options)

    # pat_rotator.py reads these from the environment at import time.
    # SAMSUNG_EMAIL/PASSWORD are the only ones we actually use (run_browser()
    # only needs these). HA_TOKEN is also required at import time even though
    # we never call push_token_to_ha() - it just needs to exist as a string,
    # its value is irrelevant to the code path we actually use.
    os.environ["SAMSUNG_EMAIL"] = options["samsung_email"]
    os.environ["SAMSUNG_PASSWORD"] = options["samsung_password"]
    os.environ.setdefault("HA_TOKEN", "unused")
    if options.get("samsung_totp_secret"):
        os.environ["SAMSUNG_TOTP_SECRET"] = options["samsung_totp_secret"]

    import pat_rotator  # noqa: E402  (must import after env vars are set)

    log.info("Starting PAT rotation via Playwright...")
    token = await pat_rotator.run_browser(debug=False)
    log.info("Got a fresh PAT, delivering to %s", options["target_service"])
    call_ha_service(options["target_service"], {options["token_field"]: token})
