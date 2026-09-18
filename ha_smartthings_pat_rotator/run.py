#!/usr/bin/env python3
"""Entry point: rotate the SmartThings PAT on a schedule, forever."""
import asyncio
import json
import logging

from rotate_and_submit import rotate_once

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("run")


async def main() -> None:
    with open("/data/options.json") as f:
        interval_hours = json.load(f)["rotate_interval_hours"]
    interval_seconds = interval_hours * 3600

    while True:
        try:
            await rotate_once()
        except Exception:
            log.exception("PAT rotation failed - will retry next cycle")
        log.info("Sleeping %s hours until next rotation", interval_hours)
        await asyncio.sleep(interval_seconds)


if __name__ == "__main__":
    asyncio.run(main())
