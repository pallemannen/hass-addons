# Home Assistant Add-on: HA USBIP Mounter

USBIP client addon to manage mounting usbip devices to home assistant

![Supports aarch64 Architecture][aarch64-shield]
![Supports amd64 Architecture][amd64-shield]

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg

## Origin

Temporary fork of [irakhlin/hassio-addons](https://github.com/irakhlin/hassio-addons)'s
`usbip-mounter-patched`, all credit to Ilya Rakhlin for the original add-on.
This copy exists only to run a fix (auto re-attach on dropped usbip connections,
see CHANGELOG) that hasn't been merged upstream yet - see
[irakhlin/hassio-addons PR](https://github.com/irakhlin/hassio-addons/pulls) for status.
**Once merged and released upstream, switch back to the original repository and
remove this folder** rather than maintaining a permanent duplicate.