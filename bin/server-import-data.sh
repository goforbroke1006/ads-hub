#!/usr/bin/env bash

source .env
export PYTHONPATH=.

python2.7 script/server/task/vk-import.py ${VK_ADS_ACCOUNT_ID} || true
python2.7 script/server/task/fb-import.py ${FB_ADS_ACCOUNT_ID} || true
