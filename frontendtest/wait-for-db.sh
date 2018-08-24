#!/usr/bin/env bash

retry_count = 10
until $(curl --output /dev/null --silent --head --fail $DBAS_PROTOCOL://$DBAS_HOST:$DBAS_PORT/discuss/cat-or-dog);
do
    if
    printf '.'
    sleep 1
done



while [retry_count != 0] && !$(curl --output /dev/null --silent --head --fail $DBAS_PROTOCOL://$DBAS_HOST:$DBAS_PORT/discuss/cat-or-dog)