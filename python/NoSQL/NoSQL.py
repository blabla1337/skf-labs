import re
from flask import Flask, render_template, request, url_for, redirect, session
from uuid import uuid4
# from bson.objectid import ObjectId

from db.db import comments, users
from json import dumps
from db.seed import seed_db


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True
app.secret_key = 'mysecret'

seed_db()


@app.route("/")
def home():
    username = None

    if "id" in session:
        user = users.find_one({"_id": session['id']})
        if user is None:
            session.clear()
            redirect(url_for('home'))

    if "username" in session:
        username = session['username']

    return render_template("index.html", user=username)


@app.route("/register/", methods=['GET', 'POST'])
def register_route():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        if username == "" or password == "":
            return dumps({"error": "Username or password cannot be empty"}, default=str), 403
        user = users.find_one(
            {"username": re.compile(username, re.IGNORECASE)})
        if user:
            error = "User already exists"
            return dumps({"error": error}, default=str), 403
        else:
            user = {"_id": uuid4().hex, "username": username,
                    "password": password}
            users.insert_one(user)
            return dumps({"message": "User created"}, default=str)


@app.route("/login/", methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = users.find_one({"username": username, "password": password})
        if user:
            session['id'] = str(user.get('_id'))
            session['username'] = user.get('username')
            return dumps({"message": "User logged in"}, default=str)
        else:
            error = "Invalid username or password"
            return dumps({"error": error}, default=str), 401


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route("/comments/", methods=['GET', 'POST', 'PUT'])
def comments_route():
    if request.method == 'GET':
        commentList = {"comments": list(comments.find())}
        return dumps((commentList), default=str)
    if request.method == 'POST':
        author = session['username']
        text = request.get_json()['text']
        comment = {"_id": uuid4().hex, "author": author, "text": text}
        comments.insert_one(comment)
        return dumps(comment, default=str)
    elif request.method == 'PUT':
        id = request.get_json()['id']
        text = request.get_json()['text']
        comments.update_many(
            #     {"_id": ObjectId(id)}, {"$set": {"text": text}})
            {"_id": id}, {"$set": {"text": text}})
        return dumps({"text": text}, default=str)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
