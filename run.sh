#!/bin/sh

# Created by Christian Meter
#
# Start postgresql, update all requirements and
# start development server of D-BAS

service=postgresql.service
active=`systemctl is-active $service`

if ! [ $active == "active"  ]
then
    echo "Starting Postgresql..."
    sudo systemctl start $service
fi

pip install -U -r requirements.txt

echo "Starting local D-BAS instance..."
pserve development.ini --reload