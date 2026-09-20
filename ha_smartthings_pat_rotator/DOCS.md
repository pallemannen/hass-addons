# Home Assistant Add-on: SmartThings PAT Rotator

It doesn't assume any particular integration - point it at whatever service
accepts a PAT.

Built alongside [ibielopolskyi/smartthings_fridge_camera](https://github.com/ibielopolskyi/smartthings_fridge_camera)
(Samsung FamilyHub Fridge), whose `update_pat` service is the default
`target_service` example below - see
[PR #45](https://github.com/ibielopolskyi/smartthings_fridge_camera/pull/45),
open upstream at the time of writing, adding that service. Until it's
merged, `update_pat` only exists on a locally patched install of that
integration.

## Setup

Every run needs a logged-in browser session to succeed - Samsung's fraud
detection blocks a cold automated login outright (see below) - so get that
in hand before the first start, not after:

1. Log into [account.smartthings.com](https://account.smartthings.com/) in
   Chrome - **required**.
2. Also log into [account.samsung.com](https://account.samsung.com/) in the
   same browser - **recommended**. SmartThings login is SSO through the
   Samsung account, so this likely helps the session survive longer; not
   confirmed to be strictly necessary on its own.
3. Run `tools/extract_samsung_cookies.py` on your own machine (see the
   script's own docstring for setup) - this writes `samsung_cookies.json`.
4. Configure the add-on (Settings → Add-ons → SmartThings PAT Rotator →
   Configuration):
   - `samsung_email` / `samsung_password` - your Samsung account credentials.
     Used only to log in via a real browser session; not sent anywhere else.
   - `samsung_totp_secret` - only needed if your account uses TOTP
     (authenticator app) 2FA. Leave blank otherwise.
   - `target_service` - the `domain.service` to call with the new token, e.g.
     `samsung_familyhub_fridge.update_pat`.
   - `token_field` - the field name that service expects the token under
     (default `token`).
   - `rotate_interval_hours` - how often to rotate (default 20, safely inside
     the 24h expiry window).
   - `cookies_json` - paste the contents of `samsung_cookies.json` from step 3.
5. Save, then start the add-on. The first run consumes and clears
   `cookies_json` automatically, seeding a working session from the start
   instead of failing on a cold login.

## Session persistence & re-seeding

Samsung's login flow reliably blocks a fully cold, cookie-less automated
login - confirmed through direct testing, it triggers a real reCAPTCHA
challenge or a phone-push MFA prompt every time, neither of which a headless
browser can solve. There is no way around this other than starting from an
actual logged-in browser session; device-recognition cookies alone (without
an active session) are not enough either - this was tested directly.

The vendored login flow itself supports a full clean login (email, password,
TOTP) from scratch every cycle just fine - it's Samsung's side that reliably
blocks it in practice. So in practice this add-on only works by keeping a
session alive rather than attempting a fresh login each cycle: every
successful rotation re-saves the browser's session (cookies) to
`/data/browser_state.json`, refreshing it before the next run. As long as
rotation keeps succeeding, this self-perpetuates indefinitely with no
further action needed.

If that session ever does expire or get invalidated (a password change, or
whatever inactivity/security policy Samsung applies - not yet known), a
persistent notification appears in Home Assistant telling you to re-seed it
rather than the add-on silently retrying against a session that can't
recover on its own. To recover:

1. Log into [account.smartthings.com](https://account.smartthings.com/) in
   Chrome on your own machine - **required**. Also log into
   [account.samsung.com](https://account.samsung.com/) in the same browser -
   **recommended** (see Setup above for why).
2. Run `tools/extract_samsung_cookies.py` there (see the script's own
   docstring for setup).
3. Paste the resulting `samsung_cookies.json` contents into the add-on's
   `cookies_json` config field and save.
4. Restart the add-on (or wait for the next retry) - it consumes the pasted
   cookies, seeds a fresh session, and clears the field automatically.

## How it works

- `pat_rotator.py` is vendored as a git submodule from
  [pallemannen/SmartThings-PAT-Rotator](https://github.com/pallemannen/SmartThings-PAT-Rotator)
  (a fork of [TryTryAgain/SmartThings-PAT-Rotator](https://github.com/TryTryAgain/SmartThings-PAT-Rotator)
  with a couple of reliability fixes on top) - all the actual login/token-
  generation logic lives there and stays upstream-trackable.
- We only call its `run_browser()` function to get a token back as a plain
  string - we never use its own `push_token_to_ha()`/`main()`, which push to
  an `input_text` helper instead. Delivering via a real HA service call is
  cleaner and doesn't require patching the consuming integration's internals.
- A separate check distinguishes a genuinely dead session (real CAPTCHA/MFA
  block - alert and stop retrying) from transient failures (a network blip,
  or the tokens page still rendering when checked - both retried
  automatically instead).

## Troubleshooting

If login starts failing, the most likely cause by far is an expired session -
see "Session persistence & re-seeding" above and check the logs for a
CAPTCHA/MFA-shaped error (e.g. `Could not find password input`,
`Login may have failed`). Re-seeding via `cookies_json` fixes this - you
should also see a persistent notification in Home Assistant pointing at
the same fix.

If that's not it, check for a Samsung UI change breaking Playwright's
selectors - see the vendored `pat_rotator.py`'s own troubleshooting notes for
the `--debug` flag and `--clear-state` option (invoke by shelling into the
add-on container).
