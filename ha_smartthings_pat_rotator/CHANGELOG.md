# Changelog

## 0.1.3
- Added retry logic: a rotation attempt now retries up to 3 times (3
  minutes apart) before falling back to the full `rotate_interval_hours`
  wait. A confirmed real-world failure was a one-off `ERR_NETWORK_CHANGED`
  during page load (page got stuck on its loading spinner, never
  rendered the login form) - the page and URL were fine on a normal
  retry, so losing a full ~20h cycle to a transient glitch wasn't
  necessary.

## 0.1.2
- Fixed a second missing-dependency issue: `pat_rotator.py` also requires
  `HA_TOKEN` to be set at import time (for its own unused
  `push_token_to_ha()`), which we never set since we don't use that
  function. Set to a harmless placeholder before import - verified with a
  build that exercises the exact same env-setup path `rotate_once()` uses.

## 0.1.1
- Fixed missing `aiohttp` and `playwright` Python packages - the base
  image only provides Chromium and its system dependencies, not these
  pip packages themselves. Rotation was failing on every run with
  `ModuleNotFoundError`.

## 0.1.0
- Initial release: rotates a SmartThings Personal Access Token via
  Playwright browser automation on a configurable schedule (default 20h,
  PATs expire after 24h) and delivers it to a configurable HA service
  (`target_service`/`token_field`) - not hardcoded to any one integration.
  Vendors `pat_rotator.py` from TryTryAgain/SmartThings-PAT-Rotator
  unmodified as a git submodule; only calls its `run_browser()`, never its
  own `input_text`-based delivery.
