#!/bin/sh

# Created by Christian Meter
#
# Start postgresql, update all requirements and
# start development server of D-BAS

service=postgresql.service

# Test if systemd or a service has to be called
pidof systemd > /dev/null && systemd=1 || systemd=0

active=`systemctl is-active $service`

if ! [ $active == "active"  ]
then
    echo "Starting Postgresql..."
    if [ $systemd != 0 ]
    then
        echo "Invoking systemd..."
        sudo systemctl start $service
    else
        echo "Invoking service..."
        sudo service $service Start
    fi
fi

pip install -U -r requirements.txt

echo "Starting local D-BAS instance..."
pserve development.ini --reload
