#!/bin/sh

if [ "$(id -u)" != "0" ]; then
    echo ":error This script must be run as root." 1>&2
    exit 1
fi

printf ":update D-BAS-deploy \n"
sudo -u krauthoff git pull

systemctl stop deploy_dbas
docker-compose rm -f
docker system prune -f
docker-compose pull
systemctl start deploy_dbas