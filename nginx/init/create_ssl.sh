#!/bin/sh
[ -d /etc/nginx/ssl ] || mkdir -p /etc/nginx/ssl
apk --update add openssl
DEPLOY_HOST=${DEPLOY_HOST#https://}
DEPLOY_HOST=${DEPLOY_HOST#http://}
openssl req -x509 -sha256 -nodes -days 3650 -newkey rsa:4096 -keyout /etc/nginx/ssl/nginx.key -out /etc/nginx/ssl/nginx.crt -subj "/CN=$DEPLOY_HOST"