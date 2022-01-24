from flask import Flask, request, url_for, render_template, redirect, Markup
import flask
import os
import subprocess
import time

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def start():
    return render_template("index2.html")


@app.route("/web", methods=['GET'])
def home():
    sleepingtime = request.args.get('numero')
    print(sleepingtime)

    return render_template("index.html", read = flask.Markup(sleepingtime))


if __name__ == "__main__":
    app.run(host='0.0.0.0')

