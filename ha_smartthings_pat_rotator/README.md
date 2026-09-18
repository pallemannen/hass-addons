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
2. Start the add-on.

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

If login starts failing, run the add-on with debug logging and check for a
Samsung UI change breaking Playwright's selectors - see the vendored
`pat_rotator.py`'s own troubleshooting notes for the `--debug` flag and
`--clear-state` option (invoke by shelling into the add-on container).
