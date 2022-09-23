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
#   In session management components, a common mistake is to include
#   specific data in the Token instead of issuing a generic value and 
#   referencing real data server-side.
#   This file implements a demo scenario for this kind of attacks.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 
# References:
#   https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Session_Management_Testing/01-Testing_for_Session_Management_Schema
# 

from models.SQL import DataAccess
from flask import Flask, request, render_template, make_response, request, redirect
import base64


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = False 


@app.route("/")
def start():
    return render_template("index.html")



@app.route("/login", methods=['GET', 'POST'])
def login():
    '''
    This function handles new login request
    '''
    if validateLoginRequest(request):
        try:

            # Data access layer may raise exceptions
            if validateUserLoginRequest(request):
                return createSuccessfulLoggedInResponse(request)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return render_template("500.html", error=str(e))

    return render_template("index.html")



@app.route("/panel", methods=['POST', 'GET'])
def panel():
    '''
    Management panel
    '''
    if not isLoggedIn(request):
        return redirect('/login')

    username = extractSessionUser(request)
    welcome_message = 'Congratulations!' if username == 'admin' else 'Welcome!'
    return render_template("loggedin.html", username=username, msg=welcome_message)



@app.route("/logout", methods=['GET'])
def logout():
    '''
    Logoff user account and clear session.
    '''
    if request.method != "GET":
        return redirect('/')

    return createSuccessfulLogoffResponse(request)



@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")



def isLoggedIn(request):
    if 'sessionid' in request.cookies:
        database = DataAccess()
        username = extractSessionUser(request)
        return database.checkUserExists(username)
    return False


def validateLoginRequest(request):
    keys = request.form.keys()
    return 'username' in keys and 'password' in keys


def getLoginRequestUsername(request):
    return request.form['username']


def validateUserLoginRequest(request):
    username = request.form['username']
    password = request.form['password']
    database = DataAccess()
    return database.validateCredentials(username, password)


def createSuccessfulLoggedInResponse(request):
    username = getLoginRequestUsername(request)
    response = make_response(redirect("/panel"))
    response.set_cookie("sessionid", base64.b64encode(username.encode()))
    return response


def createSuccessfulLogoffResponse(request):
    response = make_response(redirect("/"))
    response.set_cookie('sessionid', '', expires=0)
    return response


def extractSessionUser(request):
    encoded = request.cookies.get('sessionid')
    return base64.b64decode(encoded).decode()


if __name__ == "__main__":
    app.run(host='0.0.0.0')
