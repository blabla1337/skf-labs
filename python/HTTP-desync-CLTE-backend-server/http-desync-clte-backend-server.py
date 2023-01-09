#!/usr/bin/python
# -*- coding: utf-8 -*-
# 
# SKF Labs - Security Knowledge Framework (SKF)
# Copyright (C) 2022, OWASP Foundation, Inc.
# 
# This software is provided under a slightly modified version
# of The GNU Affero General Public License. See the accompanying LICENSE 
# file for more information.
# 
# Description:
#   This machine serves as backend .....
# 
# Author:
#   Alex Romero (@NtAlexio2)
# 
# Reference:
#   https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn
# 

import os
import logging
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

CRLF = '\r\n'


home_page_content  = b""
with open(os.path.join("templates", "index.html"), 'rb') as f:
    home_page_content = f.read()

def map_path_to_file(path):
    return path[1:].replace('/', '\\')


class ContentLengthFrontEndServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        file = map_path_to_file(self.path)
        if os.path.exists(file):
            with open(file, 'rb') as f:
                self.wfile.write(f.read())
        else:
            self.wfile.write(home_page_content)

    def do_POST(self):
        self._set_headers()

        request_body = ""
        chunk_size   = self.read_chunk_size()
        while chunk_size != 0:
            request_body += self.read_chunk(chunk_size)
            chunk_size    = self.read_chunk_size()
        terminator = self.rfile.read(len(CRLF)).decode()
        request_body += terminator

        self.wfile.write(b"It works!")
    
    def read_chunk_size(self):
        line = self.rfile.readline().strip()
        return int(line, 16)
    
    def read_chunk(self, chunk_size):
        chunk = self.rfile.read(chunk_size).decode()
        chunk += self.rfile.read(len(CRLF)).decode()
        return chunk


def run(address):
    logging.info("server started on {}".format(':'.join(map(lambda x: str(x), address))))
    httpd = HTTPServer(address, ContentLengthFrontEndServer)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(('', int(argv[1])))

    elif len(argv) == 3:
        run((argv[1], int(argv[2])))
    
    else:
        run(('', 8081))
