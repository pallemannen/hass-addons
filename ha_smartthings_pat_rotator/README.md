# SmartThings PAT Rotator

[![Open your Home Assistant instance and show the dashboard of an app.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?repository_url=https%3A%2F%2Fgithub.com%2Fpallemannen%2Fhass-addons&addon=ha_smartthings_pat_rotator)

SmartThings deprecated indefinite Personal Access Tokens on 2024-12-30 - new
PATs now expire after 24 hours. This add-on keeps one alive automatically:
it logs into `account.smartthings.com` via a headless browser
([Playwright](https://playwright.dev/)) on a schedule, generates a fresh
PAT, and delivers it to a Home Assistant service of your choice.

It doesn't assume any particular integration - point it at whatever service
accepts a PAT.

## Setup

1. Configure the add-on (Settings → Add-ons → SmartThings PAT Rotator → Configuration):
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
   - `cookies_json` - leave blank initially; see "Session persistence &
     re-seeding" below.
2. Start the add-on.
3. The very first run needs a logged-in browser session to succeed (Samsung's
   fraud detection blocks a cold automated login - see below), so seed one
   before or right after starting:
   - Log into [account.smartthings.com](https://account.smartthings.com/) in
     Chrome - **required**.
   - Also log into [account.samsung.com](https://account.samsung.com/) in
     the same browser - **recommended**. SmartThings login is SSO through
     the Samsung account, so this likely helps the session survive longer;
     not confirmed to be strictly necessary on its own.
   - Run `tools/extract_samsung_cookies.py` on your own machine, then paste
     its output into the `cookies_json` config field and save.

## Session persistence & re-seeding

Samsung's login flow reliably blocks a fully cold, cookie-less automated
login - confirmed through direct testing, it triggers a real reCAPTCHA
challenge or a phone-push MFA prompt every time, neither of which a headless
browser can solve. There is no way around this other than starting from an
actual logged-in browser session; device-recognition cookies alone (without
an active session) are not enough either - this was tested directly.

So instead, this add-on works by keeping a session alive rather than logging
in from scratch each cycle: every successful rotation re-saves the browser's
session (cookies) to `/data/browser_state.json`, refreshing it before the
next run. As long as rotation keeps succeeding, this self-perpetuates
indefinitely with no further action needed.

If that session ever does expire or get invalidated (a password change, or
whatever inactivity/security policy Samsung applies - not yet known),
rotation will start failing with a login/CAPTCHA/MFA error in the logs. To
recover:

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

- `pat_rotator.py` is vendored unmodified as a git submodule from
  [TryTryAgain/SmartThings-PAT-Rotator](https://github.com/TryTryAgain/SmartThings-PAT-Rotator) -
  all the actual login/token-generation logic lives there and stays
  upstream-trackable (`git submodule update --remote` to pull in fixes, e.g.
  if Samsung changes their login page).
- We only call its `run_browser()` function to get a token back as a plain
  string - we never use its own `push_token_to_ha()`/`main()`, which push to
  an `input_text` helper instead. Delivering via a real HA service call is
  cleaner and doesn't require patching the consuming integration's internals.

## Troubleshooting

If login starts failing, the most likely cause by far is an expired session -
see "Session persistence & re-seeding" above and check the logs for a
CAPTCHA/MFA-shaped error (e.g. `Could not find password input`,
`Login may have failed`). Re-seeding via `cookies_json` fixes this.

If that's not it, check for a Samsung UI change breaking Playwright's
selectors - see the vendored `pat_rotator.py`'s own troubleshooting notes for
the `--debug` flag and `--clear-state` option (invoke by shelling into the
add-on container).
