#!/usr/bin/env python3
import os.path
from flask import Flask, request, render_template, send_from_directory
from flask_autoindex import AutoIndex
from flask_basicauth import BasicAuth

# app = Flask(__name__, static_url_path='/static', static_folder='static')
app = Flask(__name__)
app.config['DEBUG'] = True

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin123'


basic_auth = BasicAuth(app)
# https://stackoverflow.com/a/41527903
files_index = AutoIndex(app, os.path.curdir +
                        '/backups/', add_url_rules=False)


@app.route('/backups/')
def autoindex(path='.'):
    return files_index.render_autoindex(path)


@app.route('/backups/<path:filename>')
@basic_auth.required
def backups(filename):
    return send_from_directory("/backups/", filename=filename)


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/static/img")
def static2():
    filename = "static/img/" + request.args.get('image')
    return send_from_directory("", filename)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory("", "robots.txt")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
