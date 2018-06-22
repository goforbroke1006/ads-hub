#!/usr/bin/env bash

docker-compose up -d

#docker-compose exec db createdb ads_hub_db
#docker-compose exec db psql -U root -d ads_hub_db -a -f ./migration.sql

if [[ ! -f ./server.pem ]]; then
    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes -subj "/C=Russia/ST=Saint-Petersburg/L=Saint-Petersburg/O=LOCALHOST/OU=LOCALHOST/CN=LOCALHOST"
fi

source .env

export PYTHONPATH=.

python2.7 client/vk-auth.py ${VK_CLIENT_ID} ${VK_CLIENT_SECRET}
python2.7 client/fb-auth.py ${FB_CLIENT_ID} ${FB_CLIENT_SECRET}

python2.7 script/server/task/vk-import.py ${VK_ADS_ACCOUNT_ID} || true
python2.7 script/server/task/fb-import.py ${FB_ADS_ACCOUNT_ID} || true
