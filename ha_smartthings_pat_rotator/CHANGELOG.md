# Changelog

## 0.1.9
- Added the missing LICENSE, logo.png, and Swedish translation, and
  split the README into a short overview + DOCS.md, matching the other
  add-ons in this repo. No functional change.

## 0.1.8
- Fixed the network-changed retry from 0.1.7: it only caught a thrown
  exception, but a network change mid-redirect (SmartThings -> Samsung's
  OAuth authorize URL) doesn't always make `page.goto()` raise - confirmed
  live via a real outage, Playwright let the navigation "complete" by
  landing on Chrome's own internal `chrome-error://chromewebdata/` page
  instead, so the retry never triggered and the run failed 32s later
  trying to find an email field on a page that could never have one.
  `goto_with_retry()` (in the `pallemannen/SmartThings-PAT-Rotator` fork)
  now also checks the landed URL and retries on a `chrome-error://` page,
  not just a thrown exception.
- Also fixed a related false-positive: the reauth-needed alert misfired
  on this same network-changed failure, because landing on
  `chrome-error://chromewebdata/` raises the exact same "Could not find
  email input" text as a real Samsung CAPTCHA block. `is_reauth_required()`
  now excludes any error whose message references a `chrome-error://`
  page - that's a transient navigation failure, not a dead session.

## 0.1.7
- `pat_rotator.py`'s vendored submodule now points at
  `pallemannen/SmartThings-PAT-Rotator` (a fork of the original
  `TryTryAgain/SmartThings-PAT-Rotator`) with two reliability fixes:
  retry `page.goto()` on a transient `net::ERR_NETWORK_CHANGED`, and wait
  up to 15s (was 5s) per selector for the "Generate new token" button,
  since the tokens page can still be mid-render (loading spinner) when
  `networkidle` fires - confirmed via a debug screenshot.
- Added detection for the one failure mode neither of the above can fix:
  Samsung blocking login with a real CAPTCHA/MFA challenge because the
  saved session is no longer trusted. Retrying that is pointless (same
  dead session, same challenge every time), so instead of burning the
  remaining retry attempts it now fires a persistent notification
  telling you to re-seed `cookies_json`, and clears that notification
  automatically on the next successful rotation.

## 0.1.6
- Fixed `cookies_json` not actually clearing itself after a successful
  seed, despite the README claiming it does. Root cause: `POST
  /addons/self/options` replaces the entire options object rather than
  merging, so sending only `{"cookies_json": ""}` failed schema
  validation ("Missing option 'samsung_email'...") - silently, since the
  seed itself still succeeded and only the clear step errored. Now sends
  the full current options with `cookies_json` overridden, confirmed
  working via direct testing against a live add-on.

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
