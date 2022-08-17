from models.sqlimodel import *
from flask import Flask, request, render_template, request, session, make_response, url_for, redirect
import sys
import hashlib
import datetime

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True


# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'
app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = False
))


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli  = Classes()
    values = sqli.getUser(request.form['username'])
    if values:
        if values[0][2] == request.form['password']:
            userId = str(values[0][0])
            session['loggedin'] = True
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie("userId", value=userId)
            return resp
    return render_template("index.html")


@app.route('/home')
def home():
    if not session.get('loggedin'):
        return render_template('index.html')
    sqli  = Classes()
    notes = sqli.getNotes(request.cookies.get('userId'))
    return render_template('loggedin.html', notes=notes)


@app.route("/newNote", methods=['POST', 'GET'])
def update():
    if not session.get('loggedin'):
        return render_template('index.html')
    sqli  = Classes()
    if request.method == "POST":
        sqli.newNote(request.form['title'], request.form['body'], request.cookies.get('userId'))
    notes = sqli.getNotes(request.cookies.get('userId'))
    return render_template("loggedin.html", notes = notes)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("index.html")


@app.route("/forget")
def forget():
    return render_template("forget.html")


@app.route("/passwordForget", methods=['POST'])
def reset():
    sqli  = Classes()
    values = sqli.getUser(request.form['username'])
    if values:
        if values[0][1] == request.form['username']:
            current_time = datetime.datetime.now()
            timestamp = current_time.second
            to_hash = values[0][1]+str(timestamp)
            resetToken = hashlib.sha1(to_hash.encode('utf-8')).hexdigest()
            sqli.passwordForget(values[0][1], resetToken)
            print("/reset"+"/"+request.form['username']+"/"+resetToken, file=sys.stdout)
    return render_template("index.html")


@app.route("/reset", methods=['POST'])
def resetPassword():
    sqli  = Classes()
    values = sqli.getToken(request.form['resetToken'])
    print(values, file=sys.stdout)
    if values:
        if values[0][1] == request.form['resetToken']:
            print("i got there", file=sys.stdout)
            sqli.updateUser(request.form['password'], request.form['username'])
            return render_template("index.html")
    return render_template("fail.html")


@app.route("/reset/<user>/<resetToken>")
def resetLink(user, resetToken):
    return render_template("reset.html", username=user, resetToken=resetToken)


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registerUser", methods=['POST'])
def registerUser():
    sqli  = Classes()
    if request.method == "POST":
        if request.form['password'] == request.form['repassword']:
            sqli.newUser(request.form['username'], request.form['password'])
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

