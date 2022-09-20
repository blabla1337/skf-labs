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
#   This lab represents simple demo for websocket communications
#   and how they could lead attackers to different kind of exploits.
#   Here just a simple websock echo server implemented.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 
# Refernces:
#   https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/11-Client-side_Testing/10-Testing_WebSockets
#   https://portswigger.net/web-security/websockets
# 

import os
from flask import Flask, render_template
from flask_sock import Sock

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


LOG_FILE = 'message_history.log'


# initialize websocket
sock = Sock(app)
sock.init_app(app)


@sock.route('/echo')
def echo(sock):
    '''
    Reflect back incomming message to client.
    '''
    while True:
        data = sock.receive()
        sock.send(data)
        log_message(data)


@app.route("/")
def start():
    '''
    Main page.
    '''
    return render_template("index.html", history=read_history())


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


def log_message(message):
    with open(LOG_FILE, 'a+') as log:
        log.write(message + '\n')


def read_history():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log:
            return log.read()
    return ""


if __name__ == "__main__":
    app.run(host='0.0.0.0')

