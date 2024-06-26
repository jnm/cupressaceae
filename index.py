#!/usr/bin/env python3
# jnm 20211101

import os
import subprocess
import http.server
from http import HTTPStatus
from ansi2html import Ansi2HTMLConverter

PORT = 8013

ansi_to_html = Ansi2HTMLConverter().convert
cypress_env = os.environ.copy()


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
        cypress_env['CYPRESS_URL'] = url
        try:
            print('Starting Cypress…', flush=True)
            output = subprocess.check_output(
                ['cypress', 'run'],
                stderr=subprocess.STDOUT,
                env=cypress_env,
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
