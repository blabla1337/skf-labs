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
#   A cookie must resist malicious attempts of modification. 
#   If the tester receives a cookie like IsAdmin=No, it is trivial to modify it to 
#   get administrative rights, unless the application performs a double 
#   check (for instance, appending to the cookie an encrypted hash of its value)
#   This file implements a demo scenario for this kind of attacks.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 
# References:
#   https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Session_Management_Testing/01-Testing_for_Session_Management_Schema
# 

import random
from models.SQL import DataAccess
from flask import Flask, request, render_template, make_response, request, redirect


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True


# a python dictionary resolves SessionIds to corresponding username
ACTIVE_SESSIONS = {}


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
                sessionId, response = createSuccessfulLoggedInResponse(request)
                ACTIVE_SESSIONS[sessionId] = getLoginRequestUsername(request)
                return response

        except Exception as e:
            if app.config['DEBUG']:
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

    is_admin = isAdmin(request) # vulnerable function!
    welcome_message = 'Congratulations!' if is_admin else 'Welcome!'
    username = ACTIVE_SESSIONS[getSessionKey(request)]
    return render_template("loggedin.html", username=username, msg=welcome_message, is_admin=is_admin)



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
    return 'SessionId' in request.cookies \
        and getSessionKey(request) in ACTIVE_SESSIONS.keys()


def isAdmin(request):
    return 'IsAdmin' in request.cookies \
        and (request.cookies['IsAdmin'] == '1')


def validateLoginRequest(request):
    keys = request.form.keys()
    return 'username' in keys and 'password' in keys


def getLoginRequestUsername(request):
    return request.form['username']


def getLoginRequestPassword(request):
    return request.form['password']


def getSessionKey(request):
    return request.cookies['SessionId'].encode()


def validateUserLoginRequest(request):
    username = getLoginRequestUsername(request)
    password = getLoginRequestPassword(request)
    database = DataAccess()
    return database.validateCredentials(username, password)


def isUserAdmin(username):
    try:
        database = DataAccess()
        return database.isAdmin(username)
    except Exception:
        if app.config['DEBUG']:
            import traceback
            traceback.print_exc()


def createSuccessfulLoggedInResponse(request):
    sessionId = createSessionId()
    username  = getLoginRequestUsername(request)
    isAdmin   = '1' if isUserAdmin(username) else '0'
    response = make_response(redirect("/panel"))
    response.set_cookie("SessionId", sessionId)
    response.set_cookie("IsAdmin", isAdmin.encode())
    return [sessionId, response]


def createSuccessfulLogoffResponse(request):
    try:
        sessionId = getSessionKey(request)
        ACTIVE_SESSIONS.pop(sessionId)
    except:
        pass
    response = make_response(redirect("/"))
    response.set_cookie('SessionId', '', expires=0)
    return response


def createSessionId():
    hash = random.getrandbits(128)
    return b"%032x" % hash


if __name__ == "__main__":
    app.run(host='0.0.0.0')
