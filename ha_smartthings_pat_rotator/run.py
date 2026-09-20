#!/usr/bin/env python3
"""Entry point: rotate the SmartThings PAT on a schedule, forever."""
import asyncio
import json
import logging

from rotate_and_submit import (
    alert_reauth_needed,
    dismiss_reauth_alert,
    is_reauth_required,
    rotate_once,
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


async def rotate_with_retries() -> bool:
    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            await rotate_once()
            dismiss_reauth_alert()
            return True
        except Exception as exc:
            log.exception(
                "PAT rotation attempt %s/%s failed", attempt, RETRY_ATTEMPTS
            )
            if is_reauth_required(exc):
                # A dead/CAPTCHA-blocked session fails identically every
                # time - burning the remaining attempts and their delays
                # against it wastes time without changing the outcome.
                # Only a human re-seeding fresh cookies fixes this, so
                # alert immediately instead of retrying blindly.
                log.error(
                    "Session needs re-authentication - alerting instead of "
                    "retrying against the same dead session"
                )
                alert_reauth_needed(exc)
                return False
            if attempt < RETRY_ATTEMPTS:
                log.info("Retrying in %s seconds...", RETRY_DELAY_SECONDS)
                await asyncio.sleep(RETRY_DELAY_SECONDS)
    log.error(
        "All %s rotation attempts failed - giving up until next cycle",
        RETRY_ATTEMPTS,
    )
    return False


async def main() -> None:
    with open("/data/options.json") as f:
        interval_hours = json.load(f)["rotate_interval_hours"]
    interval_seconds = interval_hours * 3600

    while True:
        await rotate_with_retries()
        log.info("Sleeping %s hours until next rotation", interval_hours)
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    asyncio.run(main())
