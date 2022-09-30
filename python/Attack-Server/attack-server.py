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
#   This machine serves as attacker controlled host to send back crafted 
#   responses to requests from target host. It is usefull in scenarios 
#   like SSRF, Host Header Injection, Cache Poisoning and etc.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 
# Reference:
#   https://portswigger.net/web-security/web-cache-poisoning/exploiting-design-flaws/lab-web-cache-poisoning-with-an-unkeyed-header
# 

from utils import remove_colors
import HTTPResponseParser

import logging
from flask import Flask, request, render_template, abort, redirect


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


RULES          = {}
DEFAULT_MSG    = "Craft a response!"
DEFAULT_RULE   = "/exploit"
DEFAULT_HEADER = "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8"
DEFAULT_BODY   = ""
LOG_FILE       = 'logs.txt'


@app.route("/", methods=['GET', 'POST'])
def main():
    '''
    Render main page that let users to define new roles.
    '''
    url = DEFAULT_RULE
    header = DEFAULT_HEADER
    body = DEFAULT_BODY
    message = DEFAULT_MSG

    if request.method == 'POST':

        action = request.form['formAction']
        url = request.form['responseFile']
        header = request.form['responseHead']
        body = request.form['responseBody']

        if action == 'STORE' and url.strip() != '':
            RULES[url] = {'header':header, 'body':body}
            message = "Rule added successfully!"

        elif action == 'VIEW_EXPLOIT':
            return redirect(url)

        elif action == 'ACCESS_LOG':
            return redirect("/logs")

    return render_template('index.html', message=message, url=url, header=header, body=body)


@app.route("/logs", methods=['GET'])
def logs():
    '''
    Access to requests history.
    '''
    logs = remove_colors(get_logs())
    return render_template('logs.html', logs=logs)


@app.route("/<path:rule>", methods=['GET', 'POST'])
def router(rule):
    '''
    Match request with defined roles and return matching responses.
    '''
    rule = '/' + rule
    if rule not in RULES.keys():
        abort(404)
    
    headers = RULES[rule]['header'].encode()
    header  = HTTPResponseParser.Parse(headers)
    body    = RULES[rule]['body']
    return body, header.getcode(), dict(header.getheaders())


@app.before_first_request
def before_first_request():
    reset_logs()
    logging.basicConfig(filename=LOG_FILE, level=logging.NOTSET)
    defaultFormatter = logging.Formatter('%(message)s')
    logging.getLogger().handlers[0].setFormatter(defaultFormatter)


def get_logs():
    with open(LOG_FILE, 'r') as logs:
        return logs.read()

def reset_logs():
    with open(LOG_FILE, 'w'): pass

if __name__ == '__main__':
    app.secret_key = "1234567890"
    app.run(debug=True, host='0.0.0.0', port=5001)
