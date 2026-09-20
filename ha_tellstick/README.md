# TellStick

[![Open your Home Assistant instance and show the dashboard of an app.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?repository_url=https%3A%2F%2Fgithub.com%2Fpallemannen%2Fhass-addons&addon=ha_tellstick)

> [!NOTE]
> Fork of [michaelarnauts/home-assistant-tellstick-addon](https://github.com/michaelarnauts/home-assistant-tellstick-addon)
> with one fix applied (`uart: true`, so a non-Duo TellStick's serial
> device is actually passed through). Upstream is unmaintained and isn't
> accepting further PRs, so this is the fix's permanent home rather than
> a fork waiting on a merge - offered upstream anyway as
> [#1](https://github.com/michaelarnauts/home-assistant-tellstick-addon/pull/1)
> in case that ever changes.

TellStick and TellStick Duo service - wraps `telldus-core` to expose
switches, lights, and sensors that communicate over 433 MHz (Nexa,
Proove, Sartano, and other TellStick-compatible protocols).

See [DOCS.md](DOCS.md) for full configuration details.

## License

Apache License 2.0, inherited from upstream - see [LICENSE](LICENSE).
