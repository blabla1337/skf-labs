from models.sqlimodel import *
from flask import Flask, request, render_template, session


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli = DbModel()
    keys = request.form.keys()
    if 'username' in keys and 'password' in keys:
        try:
            username = request.form['username']
            password = request.form['password']
            values = sqli.validateUser(username, password)
            if values:
                return render_template("loggedin.html", user = values[0][1])
        except Exception as e:
            return render_template("500.html", error=str(e))
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
