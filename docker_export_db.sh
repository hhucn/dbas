#!/bin/bash
while ! ((>/dev/tcp/db/5432) &>/dev/null)
    do
        echo "$(date) - waiting for db"
        sleep 1
    done
    echo "$(date) - db is ready, starting server"

printf "\n# Deploying D-BAS...\n"
python setup.py --quiet develop

printf "\n# Seeding discussion database...\n"
init_discussion_sql docker.ini > /dev/null 2>&1

printf "\n# Seeding news database...\n"
init_news_sql docker.ini > /dev/null 2>&1