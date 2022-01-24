from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect, make_response, request, session


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True


# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'
app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = True
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
            session['userId'] = values[0][0]
            session['loggedin'] = True
            prefc = sqli.getColor(values[0][0])
            color = prefc[0][0]
            preff = sqli.getFood(values[0][0])
            food = preff[0][0]
            return render_template("loggedin.html", color = color, food = food)
    return render_template("index.html")


@app.route("/updatecolor", methods=['POST', 'GET'])
def updatecolor():
    if not session.get('loggedin'):
        return render_template('index.html')

    sqli  = Classes()
    if request.method == "POST":
        sqli.updateColor(request.form['color'], session.get('userId'))

    prefc = sqli.getColor(session.get('userId'))
    color = prefc[0][0]
    preff = sqli.getFood(session.get('userId'))
    food = preff[0][0]

    return render_template("loggedin.html", color = color, food = food)

@app.route("/updatefood", methods=['POST', 'GET'])
def updatefood():
    if not session.get('loggedin'):
        return render_template('index.html')

    sqli  = Classes()
    if request.method == "POST":
        sqli.updateFood(request.form['food'], session.get('userId'))

    prefc = sqli.getColor(session.get('userId'))
    color = prefc[0][0]
    preff = sqli.getFood(session.get('userId'))
    food = preff[0][0]

    return render_template("loggedin.html", color = color, food = food)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

