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
#   This application is vulnerable to SQL injection attacks that causes
#   to access admin panel, without credentials.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 
# Reference:
#   https://portswigger.net/web-security/sql-injection/lab-login-bypass
# 

from models.sqlimodel import *
from flask import Flask, request, render_template, make_response, request
import hashlib


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = False 


@app.route("/")
def start():
    '''
    Application main page.
    '''
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
    Login page for users to create new session.
    '''
    sqli = dbaccess()
    keys = request.form.keys()
    if 'username' in keys and 'password' in keys:
        try:
            username = request.form['username']
            password = request.form['password']
            values   = sqli.validateUser(username, password) # Unsafe Function!
            if values:
                response = make_response(render_template("loggedin.html", username=values[0][0], msg="Congratulations!"))
                response.set_cookie("sessionid", hashlib.sha1(username.encode('utf-8')).hexdigest())
                return response
        except Exception as e:
            return render_template("500.html", error=str(e))
    return render_template("index.html")


@app.route("/loggedin", methods=['POST', 'GET'])
def loggedin():
    '''
    User dashboard.
    '''
    if not isloggedin():
        return render_template("index.html", msg='You have to login first')

    hash     = request.cookies.get('sessionid')
    sqli     = dbaccess()
    values   = sqli.getHash(hash.lower())
    username = values[0][0].lower()
    return render_template("loggedin.html", username=username, msg="Congratulations!")


@app.route("/logout", methods=['GET'])
def logout():
    '''
    Terminate user session.
    '''
    text = ''
    if request.method == "GET":
        text     = 'You successfully logged out'
        response = make_response(render_template('index.html',msg=text))
        response.set_cookie('sessionid', '', expires=0)
        return response
    text = "You are not logged out"
    return render_template('index.html', msg=text)


def isloggedin():
    if 'sessionid' in request.cookies:
        hash = request.cookies.get('sessionid')
        sqli = dbaccess()
        values = sqli.getHash(hash.lower())
        if values:
            return True
    return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

