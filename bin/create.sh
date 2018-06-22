#!/usr/bin/env bash

docker-compose up -d

sleep 8

docker-compose exec db createdb ads_hub_db
docker-compose exec db psql -U root -d ads_hub_db -a -f ./migration.sql


if [[ ! -f ./server.pem ]]; then
    openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes -subj "/C=Russia/ST=Saint-Petersburg/L=Saint-Petersburg/O=LOCALHOST/OU=LOCALHOST/CN=LOCALHOST"
fi

if [[ ! -f ./.env ]]; then
    cp .env.dist .env
    nano .env
fi
