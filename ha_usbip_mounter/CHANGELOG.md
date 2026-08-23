<!-- https://developers.home-assistant.io/docs/add-ons/presentation#keeping-a-changelog -->

## 1.0.0

- Initial release

## 1.0.1

- Fix sysfs remount to mount usbip
- Use local build on HA instead of image pull from docker

## 1.5.3

- Replace the one-shot device attach with a background loop that checks
  `usbip port` every 15s and re-attaches any device that has dropped off
  (e.g. after a `vhci_hcd: connection timed out with pending urbs` disconnect).
  Previously a dropped device required a manual add-on restart to recover,
  which also unnecessarily detached every other device the add-on manages.

## 1.5.4

- Bump build base image from `20.0.1` to `21.0.2` - the old pin had drifted
  out of sync with current Alpine package repos, breaking the build with
  apk dependency conflicts (`openssl`/`libssl3`/`libcrypto3`, `musl`/`musl-dev`).
