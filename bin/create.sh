#!/usr/bin/env bash

docker-compose up -d

docker-compose exec db createdb ads_hub_db
docker-compose exec db psql -U root -d ads_hub_db -a -f ./migration.sql
