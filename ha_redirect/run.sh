#!/usr/bin/with-contenv bashio
export TARGET_HOST=$(bashio::config 'target_host')
export TARGET_PORT=$(bashio::config 'target_port')

if bashio::config.true 'use_ssl'; then
    export SCHEME="https"
else
    export SCHEME="http"
fi

envsubst '${SCHEME} ${TARGET_HOST} ${TARGET_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx -g "daemon off;"
