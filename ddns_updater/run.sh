#!/usr/bin/with-contenv bashio

CONFIG="/data/options.json"

TSIG_ALG=$(bashio::jq "${CONFIG}" '.tsig_algorithm')
TSIG_KEYNAME=$(bashio::jq "${CONFIG}" '.tsig_keyname')
TSIG_SECRET=$(bashio::jq "${CONFIG}" '.tsig_secret')
FQDN=$(bashio::jq "${CONFIG}" '.fqdn')
ZONE=$(bashio::jq "${CONFIG}" '.zone')
BIND_SERVER=$(bashio::jq "${CONFIG}" '.bind_server')
IP_ECHO_URL=$(bashio::jq "${CONFIG}" '.ip_echo_url')
POLL_INTERVAL=$(bashio::jq "${CONFIG}" '.poll_interval')

KEY="${TSIG_ALG}:${TSIG_KEYNAME}:${TSIG_SECRET}"

bashio::log.info "Polling ${IP_ECHO_URL} every ${POLL_INTERVAL}s, updating ${FQDN} in zone ${ZONE} on ${BIND_SERVER}"

while true; do
    NEWIP=$(curl -s --max-time 10 "${IP_ECHO_URL}" || true)

    if [ -z "${NEWIP}" ]; then
        bashio::log.warning "Could not determine current public IP from ${IP_ECHO_URL}, skipping this cycle"
    else
        CURIP=$(dig +short +time=5 "${FQDN}" @"${BIND_SERVER}" || true)

        if [ "${NEWIP}" != "${CURIP}" ]; then
            bashio::log.info "IP changed: ${CURIP:-<none>} -> ${NEWIP}, sending update"
            if nsupdate <<EOF
key ${KEY}
server ${BIND_SERVER}
zone ${ZONE}
update delete ${FQDN} A
update add ${FQDN} 300 A ${NEWIP}
send
EOF
            then
                bashio::log.info "Update sent successfully"
            else
                bashio::log.warning "Update FAILED"
            fi
        fi
    fi

    sleep "${POLL_INTERVAL}"
done
