import urllib2
import sys
import webbrowser
import urlparse
import json
import os

from os.path import expanduser

print(sys.argv)

token_file_path = expanduser("~") + "/.adv-hub/vk-token"

http_port = int(sys.argv[1])
client_id = int(sys.argv[2])
client_secret = sys.argv[3] if len(sys.argv) >= 4 else None
redirect_uri = "http://localhost:%d/app_dev.php/login/check-vkontakte" % http_port

url = "https://oauth.vk.com/authorize" \
      "?client_id=%s&redirect_uri=%s&display=popup&scope=ads&response_type=token&v=5.74&state=123456" \
      % (client_id, redirect_uri)
#url = "https://oauth.vk.com/authorize?client_id=%d&display=popup&redirect_uri=%s&scope=offline,ads&response_type=code&v=5.74" \
#    % (client_id, redirect_uri)
print url

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
                    % (client_id, client_secret, params["code"])
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
#        sys.exit(0)


def run(server_class=HTTPServer, handler_class=VkAuthServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


p = Process(target=run, args=(HTTPServer, VkAuthServer, http_port,))
p.start()

webbrowser.open_new(url)

p.join()
