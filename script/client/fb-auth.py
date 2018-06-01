import json
import os
import sys
import urlparse
import webbrowser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from os.path import isdir, expanduser

import requests

BASE_FB_GRAPH_URL = "https://graph.facebook.com/v2.8"

if len(sys.argv) < 3:
    raise Exception("Script run example - "
                    + os.path.basename(__file__)
                    + " 12345 some-secret")

app_id, app_secret = sys.argv[1:3]
http_port = 8010
redirect_url = "http://localhost:%d/" % http_port

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

    os._exit(0)


class FbAuthServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print self.path
        if len(self.path.split("?")) == 2:
            data_dict = dict(urlparse.parse_qsl(self.path.split("?")[1]))
            if "code" in data_dict:
                token_url = "%s/oauth/access_token?" \
                            "client_id=%s&client_secret=%s&code=%s&redirect_uri=%s" \
                            % (BASE_FB_GRAPH_URL, app_id, app_secret, data_dict["code"], redirect_url,)
                print token_url
                res = requests.get(token_url, allow_redirects=True)
                short_lived_token = json.loads(res.text)["access_token"]
                print "Short lived: " + short_lived_token

                token_url = "%s/oauth/access_token?" \
                            "grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" \
                            % (BASE_FB_GRAPH_URL, app_id, app_secret, short_lived_token)

                res = requests.get(token_url, allow_redirects=True)

                data = json.loads(res.text)
                data["app_id"] = app_id
                data["app_secret"] = app_secret

                data_str = json.dumps(data)

                f = open(token_file_path, 'w+')
                f.write(data_str)
                f.close()

                os._exit(0)


def run(server_class=HTTPServer, handler_class=FbAuthServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


p = Process(target=run, args=(HTTPServer, FbAuthServer, http_port,))
p.start()

url = "https://www.facebook.com/v2.8/dialog/oauth?client_id=%s&redirect_uri=%s&scope=ads_read" \
      % (app_id, redirect_url)

print url
webbrowser.open_new(url)

p.join()
