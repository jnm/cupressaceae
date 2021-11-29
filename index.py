#!/usr/bin/env python3
# jnm 20211101

import os
import subprocess
import http.server
from http import HTTPStatus
from ansi2html import Ansi2HTMLConverter

PORT = 8013
CYPRESS_VOLUME = os.getcwd() + '/volume'
DOCKER_COMMAND = [
    'docker',
    'run',
    # '-it',
    '-v',
    f'{CYPRESS_VOLUME}:/yay',
    '-w',
    '/yay',
    'cypress/included:3.4.0',
]

ansi_to_html = Ansi2HTMLConverter().convert

class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            print('Starting Cypress…', flush=True)
            output = subprocess.check_output(
                DOCKER_COMMAND, stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            output = e.output
            self.send_response(HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            self.send_response(HTTPStatus.OK)
        print('Cypress finished!', flush=True)
        self.send_header('Content-Type', 'text/html; charset=UTF-8')
        self.end_headers()
        self.wfile.write(ansi_to_html(output.decode('utf-8')).encode('utf-8'))


if __name__ == '__main__':
    with http.server.ThreadingHTTPServer(
        ('', PORT), MyHTTPRequestHandler
    ) as httpd:
        print(f'Ready for service on port {PORT}.')
        httpd.serve_forever()
