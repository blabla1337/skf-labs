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
#   This machine serves as frontend server for request smuggling attack.
#   FrontEnd server acts as a proxy between user (internet) and backend
#   servers in internal network.
# 
# Author:
#   Alex Romero (@NtAlexio2)
# 
# Reference:
#   https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn
# 

from config import Config
import logging
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from requests import get, post


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


def get_backend_server():
    return Config.BACKEND_SERVER_1


class ContentLengthFrontEndServer(BaseHTTPRequestHandler):

    def do_GET(self):
        request_url = get_backend_server() + self.path[1:]
        response = get(request_url, headers=self.headers)
        self.send_status_header(response.status_code)
        self.wfile.write(response.content)

    def do_POST(self):
        request_url = get_backend_server() + self.path[1:]
        request_data = self.get_POST_data()
        response = post(request_url, data=request_data, headers=self.headers)
        self.send_status_header(response.status_code)
        self.wfile.write(response.content)

    def send_status_header(self, code):
        self.send_response(code)
        self.end_headers()

    def get_POST_data(self):
        content_len = self.get_content_length()
        post_body = self.rfile.read(content_len)
        return post_body
    
    def get_content_length(self):
        return int(self.headers.get('content-length', 0))


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
        run(('', 80))
