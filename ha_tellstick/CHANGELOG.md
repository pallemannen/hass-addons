# Changelog

## 2.2.4
- 2.2.2 and 2.2.3 never actually worked - Supervisor's schema forbids a
  tag in `image:` at all, so pinning `:2.2.1` there (2.2.3's "fix") made
  the add-on fail validation and silently disappear from the store
  entirely, rather than showing a normal error. Removed `image:` for
  good - this add-on now builds locally from its own `Dockerfile` (like
  every other add-on in this repo), which fully decouples this add-on's
  own version numbering from whatever upstream has or hasn't published.

## 2.2.3
- Fixed install failure (`404` pulling `michaelarnauts/home-assistant-tellstick-addon:2.2.2`):
  Supervisor derives the image tag from this add-on's own `version:` when
  `image:` has no tag of its own, so bumping our version past what
  upstream has ever published broke the pull. `image:` now pins
  `:2.2.1` explicitly (upstream's actual last release) so our own
  version can move independently of theirs.

## 2.2.2
- Fixed the install badge, which pointed at the wrong add-on. Added the
  missing Swedish translation.

## 2.2.1

Fork of https://github.com/michaelarnauts/home-assistant-tellstick-addon with uart: true to make the add-on app work for the original non-Duo TellStick device.

[upstream]: https://github.com/michaelarnauts/home-assistant-tellstick-addon
[upstream-pr]: https://github.com/michaelarnauts/home-assistant-tellstick-addon/pull/1
