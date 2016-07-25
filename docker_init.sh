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

    printf "\n# Seeding discussion database...\n"
    initialize_discussion_sql docker.ini > /dev/null 2>&1

    printf "\n# Seeding news database...\n"
    initialize_news_sql docker.ini > /dev/null 2>&1

    printf "\n# Seeding dummy votes...\n"
    init_discussion_testvotes docker.ini > /dev/null 2>&1

    ip=`ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1`

    printf "\n###################################################"
    printf "\n# Connect to this client via http://$ip:4284/ "
    printf "\n###################################################\n"

    printf "\n# Starting integrated web server -- for development use only!\n"
    pserve docker.ini --reload

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