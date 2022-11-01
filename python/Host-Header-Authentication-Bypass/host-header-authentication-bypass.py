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
#   In this application, there is a login page that admins
#   can enter to and manage some products. The point is 
#   admin allowed to access administration panel only from
#   local network. To achive this, develoepr used "Host" header
#   to check if request is from local network or not. But there  
#   is mistakes in implemention!
#   NOTE: This application is for demonstration purposes only.
#
# Author:
#   Alex Romero (@NtAlexio2)
# 
# Reference:
#   https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/17-Testing_for_Host_Header_Injection
# 

from db import dbmodel

from flask import Flask, request, render_template, session, redirect
import socket


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def main():
    '''
    Application main page.
    '''
    if not is_valid_application_host(request):
        return redirect('/')
    return render_template('index.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    '''
    Create new session for logging users.
    '''
    if not is_valid_application_host(request):
        return redirect('/')

    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if dbmodel.valid_login(username, password):
            session['logged_in'] = True
            return get_admin_panel()
        else:
            error = 'Invalid username/password'
    return render_template('login.html', error=error)


@app.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    '''
    Administration panel.
    '''
    if is_logged_in():
        return get_admin_panel()
    if not is_valid_application_host(request):
        return redirect('/')
    if get_hostname() == get_rqeuest_host(request):
        return render_template("login.html", error='This page is available for local users only.')
    return get_admin_panel()


@app.route("/admin/delete/<id>", methods=['POST', 'GET'])
def delete_product(id):
    '''
    Delete existing product from products page.
    '''
    message = None
    if not is_logged_in():
        if not is_valid_application_host(request):
            return redirect('/')
        if get_hostname() == get_rqeuest_host(request):
            return render_template("login.html", error='This page is available for local users only.')
        message = "You won this challange!"
    dbmodel.delete_product(id)
    return get_admin_panel(message)


@app.route("/logout")
def logout():
    '''
    Kill user session.
    '''
    if not is_valid_application_host(request):
        return redirect('/')
    session.clear()
    return redirect('/login')


def get_admin_panel(message = None):
    products = dbmodel.get_all_products()
    return render_template("dashboard.html", products=products, message=message)


def is_logged_in():
    return 'logged_in' in session and session['logged_in'] is True


def is_local_request(r):
    return get_rqeuest_host(r).lower() in ['127.0.0.1', 'localhost']


def is_valid_application_host(r):
    return is_local_request(r) or (get_hostname() == get_rqeuest_host(request))


def get_rqeuest_host(r):
    hostname = r.host
    if ':' in hostname:
        hostname = hostname.split(':')[0]
    return hostname.lower()

def get_hostname():
    return socket.gethostbyname(socket.gethostname()).lower()

if __name__ == '__main__':
    app.secret_key = "123456abcd"
    app.run(debug=True, host='0.0.0.0')
