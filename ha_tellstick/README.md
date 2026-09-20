# Home Assistant Add-on: TellStick

> [!NOTE]
> Fork of [michaelarnauts/home-assistant-tellstick-addon][upstream] with one
> fix applied: `uart: true`, so a non-Duo TellStick's serial device actually
> gets passed through. Upstream's own dependency is abandoned and the
> maintainer isn't accepting further issues or PRs (see their own deprecation
> notice below), so this fix lives here instead of waiting on a merge that
> likely won't happen. The fix is offered upstream as
> [michaelarnauts/home-assistant-tellstick-addon#1][upstream-pr] regardless,
> in case that ever changes.

> [!CAUTION]
> **Upstream deprecation notice** (from the original project)
> The library this add-on depends on is abandoned. Its last activity was 5
> years ago and it cannot be built on Alpine versions above 3.15. Users can
> continue using the add-on, but no issues or pull requests will be accepted
> upstream.

TellStick and TellStick Duo service.

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield]

## About

This add-on wraps around the `telldus-core` package to expose a service
for your TellStick and TellStick Duo.

This integration allows users to add switches, lights, and sensors which are
communicating with 433 MHz. There are a number of vendors (Capidi Elro,
Intertechno, Nexa, Proove, Sartano, and Viking) who are selling products that
work with TellStick.

For more details, please check the TellStick [protocol list][protocol-list].

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[protocol-list]: http://developer.telldus.com/wiki/TellStick_conf
[upstream]: https://github.com/michaelarnauts/home-assistant-tellstick-addon
[upstream-pr]: https://github.com/michaelarnauts/home-assistant-tellstick-addon/pull/1
