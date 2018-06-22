#!/usr/bin/env bash

source .env
export PYTHONPATH=.

python client/vk-auth.py ${VK_CLIENT_ID} ${VK_CLIENT_SECRET}
python client/fb-auth.py ${FB_CLIENT_ID} ${FB_CLIENT_SECRET}