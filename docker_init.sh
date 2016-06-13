#!/usr/bin/env bash

# check db is ready
while ! ((>/dev/tcp/db/5432) &>/dev/null)
do
  echo "$(date) - waiting for db"
  sleep 1
done
echo "$(date) - db is ready, starting server"

printf "\n# Deploying D-BAS...\n"
python setup.py develop

printf "\n# Seeding discussion database...\n"
initialize_discussion_sql docker.ini

printf "\n# Seeding news database...\n"
initialize_news_sql docker.ini

ip=`ip addr show eth0 | grep "inet\b" | awk '{print $2}' | cut -d/ -f1`

printf "\n###################################################"
printf "\n# Connect to this client via http://$ip/ "
printf "\n###################################################\n"

printf "\n# Starting integrated web server -- for development use only!\n"
pserve docker.ini --reload

echo "I feel a disturbance in the Force..."
echo ""
echo "__.-._"
echo "'-._\"7'"
echo " /'.-c"
echo " |  /T"
echo "_)_/LI"
echo ""