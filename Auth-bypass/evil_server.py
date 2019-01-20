import base64
from models.sqlimodel import *
from time import gmtime, strftime
from flask import Flask, request, url_for, render_template, redirect, make_response, session
import requests


app = Flask(__name__, static_url_path='/static', static_folder='static')

# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'
app.config.update(dict(
    SECRET_KEY= "e5ac-4ebf-03e5-9e29-a3f562e10b22",
    SESSION_COOKIE_HTTPONLY = False
))

app.config['DEBUG'] = True

@app.route("/")
def start():
    session['userId'] = 2
    session['secret'] = app.config['SECRET_KEY']
    session['loggedin'] = True
    return render_template("evil.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
	

