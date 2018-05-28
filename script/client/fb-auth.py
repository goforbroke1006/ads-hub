import json
import os
import sys
import urllib2
from os.path import isdir, expanduser

if len(sys.argv) < 3:
    raise Exception("Script run example - "
                    + os.path.basename(__file__)
                    + " 12345 some-secret")

app_id, app_secret = sys.argv[1:3]
http_port = 8010

hub_home = expanduser("~") + "/.ads-hub"
if not isdir(hub_home):
    os.makedirs(hub_home)
token_file_path = hub_home + "/fb-token"

redirect_url = "http://localhost:8010/"
url = "https://graph.facebook.com/oauth/access_token?" \
      "client_id=%s&client_secret=%s&redirect_uri=%s&" \
      "grant_type=ads_read" \
      % (app_id, app_secret, redirect_url)

# client_credentials

response = urllib2.urlopen(url)
result = json.load(response)

result["app_id"] = app_id
result["app_secret"] = app_secret

f = open(token_file_path, 'w+')
f.write(json.dumps(result))
f.close()
