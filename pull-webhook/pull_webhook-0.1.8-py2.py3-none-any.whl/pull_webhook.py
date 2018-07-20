# -*- coding: utf-8 -*-
"""Main module."""
import os
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_PORT = 8888
DEFAULT_REMOTE = "origin"
DEFAULT_BRANCH = "master"


class WebHookHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_POST(self):
        self._set_headers()
        Puller.git_pull()
        self.wfile.write("OK".encode("UTF-8", "replace"))


class Puller(object):

    remote = DEFAULT_REMOTE
    branch = DEFAULT_BRANCH
    repository_directory = os.path.dirname(os.path.abspath(__file__))

    @classmethod
    def git_pull(cls):
        print('repository directory is {}'.format(cls.repository_directory))
        print('pulling from {} branch of {} remote '.format(cls.branch, cls.remote))
        result = subprocess.call([
            "git", "--git-dir", cls.repository_directory + '/.git', "pull",
            cls.remote, cls.branch
        ])
        if result == 0:
            print("DONE")
        else:
            print("RETURN CODE IS NOT 0 BUT " + str(result))


def main(port=DEFAULT_PORT):
    server_address = ('', port)
    httpd = HTTPServer(server_address, WebHookHandler)
    print('httpd is waiting for POST requests on port {}'.format(port))
    httpd.serve_forever()


if __name__ == '__main__':
    main()
