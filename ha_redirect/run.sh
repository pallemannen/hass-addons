#!/usr/bin/with-contenv bashio
TARGET_HOST=$(bashio::config 'target_host')
TARGET_PORT=$(bashio::config 'target_port')

for PORT in 80 8080 443 8443 8123; do
    socat TCP-LISTEN:${PORT},fork,reuseaddr TCP:${TARGET_HOST}:${TARGET_PORT} &
done

wait
