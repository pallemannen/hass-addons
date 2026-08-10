#!/usr/bin/with-contenv bashio
export INTERNAL_HOST=$(bashio::config 'internal_target_host')
export INTERNAL_PORT=$(bashio::config 'internal_target_port')
export EXTERNAL_HOST=$(bashio::config 'external_target_host')
export EXTERNAL_PORT=$(bashio::config 'external_target_port')

if bashio::config.true 'use_ssl'; then
    export SCHEME="https"
else
    export SCHEME="http"
fi

envsubst '${SCHEME} ${INTERNAL_HOST} ${INTERNAL_PORT} ${EXTERNAL_HOST} ${EXTERNAL_PORT}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

nginx -g "daemon off;"
