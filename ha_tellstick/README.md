# Home Assistant Add-on: TellStick

[![Open your Home Assistant instance and show the dashboard of an app.](https://my.home-assistant.io/badges/supervisor_addon.svg)](https://my.home-assistant.io/redirect/supervisor_addon/?repository_url=https%3A%2F%2Fgithub.com%2Fpallemannen%2Fhass-addons&addon=ha_tellstick)

TellStick and TellStick Duo service.

![Supports aarch64 Architecture][aarch64-shield] ![Supports amd64 Architecture][amd64-shield]

## About

This add-on wraps around the `telldus-core` package to expose a service
for your TellStick and TellStick Duo.

This integration allows users to add switches, lights, and sensors which are
communicating with 433 MHz. There are a number of vendors (Capidi Elro,
Intertechno, Nexa, Proove, Sartano, and Viking) who are selling products that
work with TellStick.

Fork of https://github.com/michaelarnauts/home-assistant-tellstick-addon with uart: true to make the add-on app work for the original non-Duo TellStick device.

For more details, please check the TellStick [protocol list][protocol-list].

[aarch64-shield]: https://img.shields.io/badge/aarch64-yes-green.svg
[amd64-shield]: https://img.shields.io/badge/amd64-yes-green.svg
[protocol-list]: http://developer.telldus.com/wiki/TellStick_conf
[upstream]: https://github.com/michaelarnauts/home-assistant-tellstick-addon
[upstream-pr]: https://github.com/michaelarnauts/home-assistant-tellstick-addon/pull/1
