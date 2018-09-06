#!/bin/sh

[ -d /etc/nginx/ssl ] || mkdir -p /etc/nginx/ssl
apk --update add openssl
openssl req -x509 -sha256 -nodes -days 3650 -newkey rsa:4096 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/CN=${DEPLOY_HOST}"