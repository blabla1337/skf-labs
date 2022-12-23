from models.sqlimodel import *
from flask import Flask, request, render_template, request, session


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True

app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = True
))
# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'



@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login_insecure", methods=['GET', 'POST'])
def login_insecure():
    sqli  = Classes()
    values = sqli.getUser(request.form['username'])
    if values:
        if values[0][2] == request.form['password']:
            session['userId'] = values[0][0]
            session['loggedin'] = True
            pref = sqli.getColor(values[0][0])
            color = pref[0][0]
            return render_template("loggedin.html", color = color)
    return render_template("index.html")

@app.route("/login_strict", methods=['GET', 'POST'])
def login_strict():
    app.config.update(dict(
    SESSION_COOKIE_SAMESITE = 'Strict'
))
    sqli  = Classes()
    values = sqli.getUser(request.form['username'])
    if values:
        if values[0][2] == request.form['password']:
            session['userId'] = values[0][0]
            session['loggedin'] = True
            pref = sqli.getColor(values[0][0])
            color = pref[0][0]
            return render_template("loggedin.html", color = color)
    return render_template("index.html")

@app.route("/login_lax", methods=['GET', 'POST'])
def login_lax():
    app.config.update(dict(
    SESSION_COOKIE_SAMESITE = 'Lax'
))
    sqli  = Classes()
    values = sqli.getUser(request.form['username'])
    if values:
        if values[0][2] == request.form['password']:
            session['userId'] = values[0][0]
            session['loggedin'] = True
            pref = sqli.getColor(values[0][0])
            color = pref[0][0]
            return render_template("loggedin.html", color = color)
    return render_template("index.html")

@app.route("/update", methods=['POST', 'GET'])
def update():
    if not session.get('loggedin'):
        return render_template('index.html')
    sqli  = Classes()

    if request.method == "POST":
        sqli.updateColor(request.form['color'], session.get('userId'))

    if request.method == "GET" and (request.args.get('color') is not None):
             sqli.updateColor(request.args['color'], session.get('userId'))

    pref = sqli.getColor(session.get('userId'))
    color = pref[0][0]
    return render_template("loggedin.html", color = color)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

