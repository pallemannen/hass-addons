# Changelog

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
