#!/usr/bin/with-contenv bashio
TARGET_PORT=$(bashio::config 'target_port')
LISTEN_PORTS=$(bashio::config 'listen_ports')

is_valid_port() {
    case "$1" in
        ''|*[!0-9]*) return 1 ;;
    esac
    [ "$1" -ge 1 ] && [ "$1" -le 65535 ]
}

IFS=',' read -ra PORTS <<< "$LISTEN_PORTS"
for PORT in "${PORTS[@]}"; do
    PORT=$(echo "$PORT" | tr -d '[:space:]')

    if ! is_valid_port "$PORT"; then
        bashio::log.warning "Ignoring invalid listen port entry: '${PORT}'"
        continue
    fi

    if [ "$PORT" = "$TARGET_PORT" ]; then
        bashio::log.warning "Skipping listen port ${PORT} - matches target_port"
        continue
    fi

    (
        socat TCP-LISTEN:${PORT},fork,reuseaddr TCP:127.0.0.1:${TARGET_PORT}
        bashio::log.warning "Listener on port ${PORT} exited (likely already in use by another process) - other ports are unaffected"
    ) &
    bashio::log.info "Forwarding ${PORT} -> 127.0.0.1:${TARGET_PORT}"
done

wait
