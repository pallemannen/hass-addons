ARG BUILD_FROM
FROM $BUILD_FROM

RUN apk add --no-cache nginx gettext

COPY nginx.conf.template /etc/nginx/nginx.conf.template
COPY run.sh /
RUN chmod a+x /run.sh
