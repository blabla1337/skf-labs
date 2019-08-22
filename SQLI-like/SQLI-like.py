from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@app.route("/home/<username>", methods=['GET'])
def inject(username):
    sqli  = User()
    values = sqli.getUser(username)
    username = values[0][0]
    email = values[0][1]
    return render_template("index.html", username = username, email = email)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
<<<<<<< HEAD


if __name__ == "__main__":
    app.run(host='0.0.0.0')


#UNION SELECT 1,username,password FROM users
