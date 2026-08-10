# Changelog

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
