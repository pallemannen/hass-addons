# SmartThings PAT Rotator

[![Open your Home Assistant instance and show the dashboard of an app.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?repository_url=https%3A%2F%2Fgithub.com%2Fpallemannen%2Fhass-addons&addon=ha_smartthings_pat_rotator)

SmartThings deprecated indefinite Personal Access Tokens on 2024-12-30 - new
PATs now expire after 24 hours. This add-on keeps one alive automatically:
it logs into `account.smartthings.com` via a headless browser on a
schedule, generates a fresh PAT, and delivers it to a Home Assistant
service of your choice.

See [DOCS.md](DOCS.md) for full setup and configuration details.

## License

MIT - see [LICENSE](LICENSE). Vendors `pat_rotator.py` as a git submodule
from [pallemannen/SmartThings-PAT-Rotator](https://github.com/pallemannen/SmartThings-PAT-Rotator)
(a fork of [TryTryAgain/SmartThings-PAT-Rotator](https://github.com/TryTryAgain/SmartThings-PAT-Rotator)),
which carries its own separate license.
