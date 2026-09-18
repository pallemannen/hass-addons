# Changelog

## 0.1.5
- Fixed a YAML syntax error in `translations/en.yaml` that silently broke
  every config field label/description in the UI, not just one: an
  unquoted `Default: X.` mid-sentence is invalid YAML (a bare colon-space
  inside a plain scalar reads as a new mapping key), so the whole file
  failed to parse. Reworded to "Defaults to X." to avoid the embedded
  colon.
- Also clarified in the README and `tools/extract_samsung_cookies.py` that
  logging into account.smartthings.com is required and account.samsung.com
  is recommended (but unconfirmed as strictly necessary alone) before
  re-seeding a session.

## 0.1.4
- Added a `cookies_json` config option: paste the output of the new
  `tools/extract_samsung_cookies.py` (run on your own machine, reading
  Chrome's cookie store) to (re)seed a logged-in browser session. Consumed
  and cleared automatically after use.
- This exists because direct testing confirmed Samsung's login flow reliably
  blocks a fully cold, cookie-less automated login (a real reCAPTCHA or
  phone-push MFA challenge every time) - device-recognition cookies alone,
  without an active session, aren't sufficient either. A real session has to
  originate from an actual logged-in browser; this add-on can only keep one
  alive (self-refreshing it on every successful rotation), not create one
  from nothing.
- README expanded with a "Session persistence & re-seeding" section
  documenting this and the recovery steps.

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
