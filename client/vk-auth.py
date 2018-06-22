import json
import os
import sys
import urllib2
import urlparse
import webbrowser
from os.path import expanduser
from os.path import isdir

VK_API_VERSION = "5.74"

# hub_home = expanduser("~") + "/.ads-hub"
hub_home = "./.auth"
if not isdir(hub_home):
    os.makedirs(hub_home)
token_file_path = hub_home + "/vk-token"

client_id = int(sys.argv[1])
client_secret = sys.argv[2] if len(sys.argv) >= 3 else None
http_port = int(sys.argv[3]) if len(sys.argv) >= 4 else 8082
redirect_uri = "http://localhost:%d/app_dev.php/login/check-vkontakte" % http_port

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process


class VkAuthServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print self.path
        if len(self.path.split("?")) == 2:
            data_dict = dict(urlparse.parse_qsl(self.path.split("?")[1]))
            if "code" in data_dict:
                token_url = "https://oauth.vk.com/access_token?client_id=%d&client_secret=%s&redirect_uri=&code=%s" \
                            % (client_id, client_secret, data_dict["code"])
                res = urllib2.urlopen(token_url)

                f = open(token_file_path, 'w+')
                f.write(res)
                f.close()

                os._exit(0)

        self._set_headers()
        self.wfile.write(
            "<html>"
            + "<body>"
            + "  <h1>Store token!</h1>"
            + "  <script>var xhr = new XMLHttpRequest();"
            + "    var body = window.location.hash.substr(1);"
            + "    xhr.open('POST', window.location.href, true);"
            + "    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');"
            + "    xhr.onreadystatechange = function() {"
              "      alert('Saved!!');"
              "    };"
            + "    xhr.send(body);"
            + "  </script>"
            + "</body>"
            + "</html>")

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data_dict = dict(urlparse.parse_qsl(post_data))
        print data_dict

        f = open(token_file_path, 'w+')
        f.write(json.dumps(data_dict))
        f.close()

        self.wfile.write(
            "<html>"
            + "<body>"
            + "  <h1>Successfully!</h1>"
            + "</body>"
            + "</html>")

        os._exit(0)


def run(server_class=HTTPServer, handler_class=VkAuthServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


p = Process(target=run, args=(HTTPServer, VkAuthServer, http_port,))
p.start()

url = "https://oauth.vk.com/authorize" \
      "?client_id=%s&redirect_uri=%s&display=popup&scope=offline,ads&response_type=token&v=%s&state=" \
      % (client_id, redirect_uri, VK_API_VERSION)
print url
webbrowser.open_new(url)

p.join()
