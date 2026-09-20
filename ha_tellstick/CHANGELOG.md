# Changelog

## 2.2.1

- Forked from [michaelarnauts/home-assistant-tellstick-addon][upstream]
  (same version) and moved into this repo. Upstream is unmaintained (its
  dependency library is abandoned, no further issues or PRs accepted), and
  the `uart: true` fix was never going to get merged there, so this is now
  the fix's permanent home rather than a temporary fork waiting on a merge.
  The standalone fork (`pallemannen/home-assistant-tellstick-addon`) stays
  up separately for now, only to keep the upstream PR
  ([#1][upstream-pr]) alive in case the maintainer reconsiders.
- Carries the one fix on top of upstream 2.2.1: `uart: true`, so a non-Duo
  TellStick's `/dev/ttyUSB*` serial device is actually passed through to
  the add-on container.

[upstream]: https://github.com/michaelarnauts/home-assistant-tellstick-addon
[upstream-pr]: https://github.com/michaelarnauts/home-assistant-tellstick-addon/pull/1
