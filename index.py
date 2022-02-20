#!/usr/bin/env python3
# jnm 20211101

import os
import subprocess
import http.server
from http import HTTPStatus
from ansi2html import Ansi2HTMLConverter

PORT = 8013
CYPRESS_VOLUME = os.getcwd() + '/volume'

ansi_to_html = Ansi2HTMLConverter().convert

def docker_command(url, username, password):
    return [
        'docker', 'run',
        # '-it',
        '-rm',
        '-v', f'{CYPRESS_VOLUME}:/yay',
        '-w', '/yay',
        '-e', f'CYPRESS_URL={url}',
        '-e', f'CYPRESS_USERNAME={username}',
        '-e', f'CYPRESS_PASSWORD={password}',
        'cypress/included:3.4.0',
    ]


class MyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.strip('/')
        if path == 'hhi':
            url = 'https://kf.kobotoolbox.org/'
        elif path == 'ocha':
            url = 'https://kobo.humanitarianresponse.info/'
        elif path == '':
            self.send_response(HTTPStatus.NOT_FOUND)
            self.send_header('Content-Type', 'text/plain; charset=UTF-8')
            self.end_headers()
            self.wfile.write('Please specify a target'.encode('utf-8'))
            return
        else:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            print('Starting Cypress…', flush=True)
            output = subprocess.check_output(
                docker_command(
                    url,
                    os.environ['CYPRESS_USERNAME'],
                    os.environ['CYPRESS_PASSWORD'],
                ),
                stderr=subprocess.STDOUT,
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
