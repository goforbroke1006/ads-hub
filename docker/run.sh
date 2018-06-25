#!/usr/bin/env bash

cd /app

#export PYTHONPATH=/app

#source .env
cron
crontab /var/spool/cron/crontabs/ad-hub-cron

tail -f /dev/null