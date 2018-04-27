import sys
import webbrowser
import urlparse
import json

from os.path import expanduser

print(sys.argv)

http_port = int(sys.argv[1])
client_id = sys.argv[2]
redirect_uri = "http://localhost:%d/app_dev.php/login/check-vkontakte" % http_port

url = "https://oauth.vk.com/authorize" \
      "?client_id=%s&redirect_uri=%s&display=popup&scope=offline,ads&response_type=token&v=5.74&state=123456" \
      % (client_id, redirect_uri)

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process


class VkAuthServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
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
        # self._set_headers()

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        data_dict = dict(urlparse.parse_qsl(post_data))
        print data_dict

        f = open(expanduser("~") + '/.adv-hub/vk-token', 'w+')
        f.write(json.dumps(data_dict))
        f.close()

        self.wfile.write(
            "<html>"
            + "<body>"
            + "  <h1>Successfully!</h1>"
            + "</body>"
            + "</html>")

        sys.exit(0)


def run(server_class=HTTPServer, handler_class=VkAuthServer, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


p = Process(target=run, args=(HTTPServer, VkAuthServer, http_port,))
p.start()

webbrowser.open_new(url)

p.join()
