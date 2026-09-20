#!/usr/bin/env python3
"""Entry point: rotate the SmartThings PAT on a schedule, and ping the
saved session hourly in between so it doesn't go idle-stale before the
next rotation is even due."""
import asyncio
import json
import logging

from rotate_and_submit import (
    alert_reauth_needed,
    dismiss_reauth_alert,
    is_reauth_required,
    keep_alive_once,
    rotate_once,
    seconds_since_last_rotation,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("run")

# A single rotation attempt can fail for reasons that have nothing to do
# with the login flow itself - a one-off network hiccup mid-page-load, for
# example. Losing a full rotate_interval_hours cycle (default 20h) to that
# is risky given PATs expire after 24h, so retry a few times, a short wait
# apart, before actually falling back to the long sleep.
RETRY_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 180

# A CAPTCHA/MFA-shaped block doesn't necessarily mean the session is dead -
# confirmed live, one occurred and the very next hourly attempt went through
# clean with no cookie reseed. So retry those too, an hour apart (cheap
# against a 20h cadence), and only alert if it's still happening after
# REAUTH_RETRY_ATTEMPTS in a row.
REAUTH_RETRY_ATTEMPTS = 3
REAUTH_RETRY_DELAY_SECONDS = 3600

KEEP_ALIVE_INTERVAL_SECONDS = 3600

# Rotation and the keep-alive ping both drive a Playwright browser against
# the same saved session file (/data/browser_state.json) - serialize them
# so a ping never overlaps a real rotation and races writing that file.
browser_lock = asyncio.Lock()


async def rotate_with_retries() -> bool:
    transient_attempt = 0
    reauth_attempt = 0
    while True:
        try:
            async with browser_lock:
                await rotate_once()
            dismiss_reauth_alert()
            return True
        except Exception as exc:
            log.exception("PAT rotation attempt failed")
            if is_reauth_required(exc):
                reauth_attempt += 1
                if reauth_attempt >= REAUTH_RETRY_ATTEMPTS:
                    log.error(
                        "CAPTCHA/MFA block persisted across %s attempts an "
                        "hour apart - alerting instead of retrying further",
                        REAUTH_RETRY_ATTEMPTS,
                    )
                    alert_reauth_needed(exc)
                    return False
                log.warning(
                    "CAPTCHA/MFA block (%s/%s) - retrying in %s hour(s)",
                    reauth_attempt,
                    REAUTH_RETRY_ATTEMPTS,
                    REAUTH_RETRY_DELAY_SECONDS // 3600,
                )
                await asyncio.sleep(REAUTH_RETRY_DELAY_SECONDS)
                continue
            transient_attempt += 1
            if transient_attempt >= RETRY_ATTEMPTS:
                log.error(
                    "All %s rotation attempts failed - giving up until next cycle",
                    RETRY_ATTEMPTS,
                )
                return False
            log.info("Retrying in %s seconds...", RETRY_DELAY_SECONDS)
            await asyncio.sleep(RETRY_DELAY_SECONDS)


async def rotate_loop() -> None:
    with open("/data/options.json") as f:
        interval_hours = json.load(f)["rotate_interval_hours"]
    interval_seconds = interval_hours * 3600

    # A restart shouldn't force a fresh rotation against a PAT that's still
    # well within its 24h life - only rotate immediately if it's actually
    # due; otherwise wait out the rest of this cycle first.
    elapsed = seconds_since_last_rotation()
    if elapsed is not None and elapsed < interval_seconds:
        remaining = interval_seconds - elapsed
        log.info(
            "Current PAT is only %.1fh old (interval is %sh) - waiting "
            "%.1fh before rotating instead of rotating on startup",
            elapsed / 3600, interval_hours, remaining / 3600,
        )
        await asyncio.sleep(remaining)

    while True:
        await rotate_with_retries()
        log.info("Sleeping %s hours until next rotation", interval_hours)
        await asyncio.sleep(interval_seconds)


async def keep_alive_loop() -> None:
    while True:
        await asyncio.sleep(KEEP_ALIVE_INTERVAL_SECONDS)
        try:
            async with browser_lock:
                alive = await keep_alive_once()
            log.info(
                "Keep-alive ping: session %s", "still alive" if alive else "not active"
            )
        except Exception:
            log.exception("Keep-alive ping failed")


async def main() -> None:
    await asyncio.gather(rotate_loop(), keep_alive_loop())


if __name__ == "__main__":
    asyncio.run(main())
