#!/usr/bin/env bash

createdb ads_hub_db
psql -U root -d ads_hub_db -a -f ./migration.sql
