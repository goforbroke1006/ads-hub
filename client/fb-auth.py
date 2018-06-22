import json
import os
import requests
import ssl
import sys
import urlparse
import webbrowser
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from os.path import isdir, isfile

CERT_FILE_PATH = './../server.pem'

BASE_FB_GRAPH_URL = "https://graph.facebook.com/v2.11"

if not isfile(CERT_FILE_PATH):
    raise Exception("At first you should create PEM file - \n\t"
                    "$ openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes")

if len(sys.argv) < 3:
    raise Exception("Script run example -\n\n$ %s <APP_ID> <APP_SECRET>" % os.path.basename(__file__))

app_id, app_secret = sys.argv[1:3]
http_port = 4443
redirect_url = "https://localhost:%d/" % http_port

# hub_home = expanduser("~") + "/.ads-hub"
hub_home = "./.auth"
if not isdir(hub_home):
    os.makedirs(hub_home)
token_file_path = hub_home + "/fb-token"


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
                print res.text
                if res.status_code != 200:
                    print res.status_code
                    os._exit(1)
                short_lived_token = json.loads(res.text)["access_token"]
                print "Short lived: " + short_lived_token

                token_url = "%s/oauth/access_token?" \
                            "grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s" \
                            % (BASE_FB_GRAPH_URL, app_id, app_secret, short_lived_token)

                res = requests.get(token_url, allow_redirects=True)

                data = json.loads(res.text)
                print "Long lived: " + data["access_token"]

                data["app_id"] = app_id
                data["app_secret"] = app_secret

                data_str = json.dumps(data)

                f = open(token_file_path, 'w+')
                f.write(data_str)
                f.close()

                self._set_headers()
                self.wfile.write(
                    "<html>"
                    + "<body>"
                    + "  <h1>Store token!</h1>"
                    + "  <h2>Success!!</h2>"
                    + data_str
                    + "</body>"
                    + "</html>")

                os._exit(0)


def run(server_class=HTTPServer, handler_class=FbAuthServer, port=4443):
    server_address = ('', port)

    httpd = server_class(server_address, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket, certfile=CERT_FILE_PATH, server_side=True)
    print 'Starting httpd...'

    httpd.serve_forever()


p = Process(target=run, args=(HTTPServer, FbAuthServer, http_port,))
p.start()

reading_scopes = (
    "ads_read",
    "ads_management",
    # "business_management",
    # "read_audience_network_insights", "read_insights",
    # "manage_pages", "pages_manage_cta", "pages_manage_instant_articles", "pages_show_list", "read_page_mailboxes",
)
url = "https://www.facebook.com/v2.8/dialog/oauth?" \
      "client_id=%s&redirect_uri=%s&scope=%s" \
      % (app_id, redirect_url, ",".join(reading_scopes))

print url
webbrowser.open_new(url)

p.join()
