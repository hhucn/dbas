#!/usr/bin/env bash

while true; do

    # check db is ready
    while ! ((>/dev/tcp/db/5432) &>/dev/null)
    do
        echo "$(date) - waiting for db"
        sleep 1
    done
    echo "$(date) - db is ready, starting server"

    printf "\n# Deploying D-BAS...\n"
    python setup.py --quiet develop

    printf "\n# Seeding news database...\n"
    init_news_sql production.ini #> /dev/null 2>&1

    printf "\n# Compiling JS files...\n"
    google-closure-compiler-js --createSourceMap --compilationLevel SIMPLE ./dbas/static/js/{main,ajax,discussion,review}/*.js > dbas/static/js/dbas.min.js

    printf "\n# Compiling SASS files...\n"
    sass dbas/static/css/main.sass dbas/static/css/main.css --style compressed
    rm -r .sass-cache

    printf "\n# Starting uwsgi -- for production use only!\n"
    uwsgi --ini-paste production.ini

    echo ""
    echo "      ---------------------------------------"
    echo "     < A disturbance in the Force, I sense... >"
    echo "      ---------------------------------------"
    echo "        /"
    echo "       /"
    echo "      /"
    echo "__.-._"
    echo "'-._\"7'"
    echo " /'.-c"
    echo " |  /T"
    echo "_)_/LI"
    echo ""

    sleep 3

done
