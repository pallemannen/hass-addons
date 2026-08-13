#!/usr/bin/with-contenv bashio

is_valid_port() {
    case "$1" in
        ''|*[!0-9]*) return 1 ;;
    esac
    [ "$1" -ge 1 ] && [ "$1" -le 65535 ]
}

CONFIG=$(bashio::app.config)

while IFS= read -r FORWARD; do
    TARGET_HOST=$(bashio::jq "${FORWARD}" '.target_host')
    TARGET_PORT=$(bashio::jq "${FORWARD}" '.target_port')
    SOURCE_PORTS=$(bashio::jq "${FORWARD}" '.source_ports')

    IFS=',' read -ra PORTS <<< "$SOURCE_PORTS"
    for PORT in "${PORTS[@]}"; do
        PORT=$(echo "$PORT" | tr -d '[:space:]')

        if ! is_valid_port "$PORT"; then
            bashio::log.warning "Ignoring invalid listen port entry: '${PORT}'"
            continue
        fi

        if [ "$PORT" = "$TARGET_PORT" ] && { [ "$TARGET_HOST" = "localhost" ] || [ "$TARGET_HOST" = "127.0.0.1" ]; }; then
            bashio::log.warning "Skipping listen port ${PORT} - would forward to itself"
            continue
        fi

        (
            socat TCP-LISTEN:${PORT},fork,reuseaddr TCP:${TARGET_HOST}:${TARGET_PORT}
            bashio::log.warning "Listener on port ${PORT} exited (likely already in use by another process) - other listeners are unaffected"
        ) &
        bashio::log.info "Forwarding ${PORT} -> ${TARGET_HOST}:${TARGET_PORT}"
    done
done < <(bashio::jq "${CONFIG}" '.forwards[]')

wait
