#!/usr/bin/env bash

# check db is ready
while ! ((>/dev/tcp/db/5432) &>/dev/null)
do
  echo "$(date) - waiting for db"
  sleep 1
done
echo "$(date) - db is ready, starting server"

echo "Deploying D-BAS..."
python setup.py develop

echo "# Seeding discussion database..."
initialize_discussion_sql development.ini

echo "# Seeding news database..."
initialize_news_sql development.ini

echo "# Starting integrated web server -- for development use only!"
pserve development.ini --reload

echo "I feel a disturbance in the Force..."