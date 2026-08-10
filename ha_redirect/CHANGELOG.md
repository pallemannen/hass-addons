# Changelog

## 1.1.0
- BREAKING: replaced `target_host`/`target_port` with separate
  `internal_target_host`/`internal_target_port` and
  `external_target_host`/`external_target_port`, so LAN and non-LAN
  clients can be redirected to different destinations
- Added source-IP-based LAN detection (private ranges vs everything else)

## 1.0.2
- Added `use_ssl` option to control redirect scheme
- Added configurable listener ports: 80, 8080, 443, 8443, 8123 (independently
  toggleable via the Network section)
- Removed deprecated `build.yaml` in favor of Dockerfile-native build args

## 1.0.1
- Made destination host/port configurable via add-on options instead of
  hardcoded in the image

## 1.0.0
- Initial release: fixed redirect to a single host on ports 80/443
