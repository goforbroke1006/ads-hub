import json
import os
import sys
from os.path import isdir, expanduser

import requests

BASE_FB_GRAPH_URL = "https://graph.facebook.com/v2.8"

if len(sys.argv) < 3:
    raise Exception("Script run example - "
                    + os.path.basename(__file__)
                    + " 12345 some-secret")

app_id, app_secret = sys.argv[1:3]

hub_home = expanduser("~") + "/.ads-hub"
if not isdir(hub_home):
    os.makedirs(hub_home)
token_file_path = hub_home + "/fb-token"

if os.path.isfile(token_file_path):
    auth_config = json.load(open(token_file_path, 'r'))

    token_url = "%s/oauth/access_token?" \
                "grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" \
                % (BASE_FB_GRAPH_URL, app_id, app_secret, auth_config["access_token"])

    res = requests.get(token_url, allow_redirects=True)

    data = json.loads(res.text)
    data["app_id"] = app_id
    data["app_secret"] = app_secret

    data_str = json.dumps(data)

    f = open(token_file_path, 'w+')
    f.write(data_str)
    f.close()
