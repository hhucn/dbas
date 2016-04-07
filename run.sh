#!/bin/sh

# Created by Christian Meter
#
# Start postgresql, update all requirements and
# start development server of D-BAS

echo "Starting local D-BAS instance..."
sudo systemctl start postgresql.service
pip install -U -r requirements.txt
pserve development.ini --reload
