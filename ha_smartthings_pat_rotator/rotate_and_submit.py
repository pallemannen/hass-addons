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
import sys

import requests

log = logging.getLogger("rotate_and_submit")


def load_options() -> dict:
    with open("/data/options.json") as f:
        return json.load(f)


def call_ha_service(target_service: str, token_field: str, token: str) -> None:
    domain, service = target_service.split(".", 1)
    supervisor_token = os.environ["SUPERVISOR_TOKEN"]
    url = f"http://supervisor/core/api/services/{domain}/{service}"
    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {supervisor_token}",
            "Content-Type": "application/json",
        },
        json={token_field: token},
        timeout=30,
    )
    resp.raise_for_status()
    log.info("Delivered new PAT to %s successfully", target_service)


async def rotate_once() -> None:
    options = load_options()

    # pat_rotator.py reads these from the environment at import time.
    os.environ["SAMSUNG_EMAIL"] = options["samsung_email"]
    os.environ["SAMSUNG_PASSWORD"] = options["samsung_password"]
    if options.get("samsung_totp_secret"):
        os.environ["SAMSUNG_TOTP_SECRET"] = options["samsung_totp_secret"]

    import pat_rotator  # noqa: E402  (must import after env vars are set)

    log.info("Starting PAT rotation via Playwright...")
    token = await pat_rotator.run_browser(debug=False)
    log.info("Got a fresh PAT, delivering to %s", options["target_service"])
    call_ha_service(options["target_service"], options["token_field"], token)
