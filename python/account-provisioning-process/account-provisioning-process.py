# import re
from flask import Flask, render_template, request, url_for, redirect, session, send_from_directory, make_response
from json import dumps


from db.db import seed_db
from db.users import get_user_by_id, get_user, get_user_by_username, create_user, get_customers
from db.comments import get_comments, create_comment, update_comment


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True
app.secret_key = 'mysecret'


seed_db()


@app.route("/")
def home():
    username = None
    role = "guest"

    if "id" in session:
        user = get_user_by_id(session['id'])
        if user is None:
            session.clear()
            redirect(url_for('home'))
        else:
            user = get_user_by_id(session['id'])
            if user:
                role = user["role"]

    if "username" in session:
        username = session['username']

    if "id" not in session:
        res = make_response(render_template("index.html", user=username))
        res.set_cookie('role', 'guest')
        return res

    return render_template("index.html", user=username, role=role)


@app.route("/register/", methods=['GET', 'POST'])
def register_route():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = get_user_by_username(username)
        if user:
            error = "User already exists"
            return dumps({"error": error}, default=str), 403
        else:
            create_user(username, password)
            return dumps({"message": "User created"}, default=str)


@app.route("/login/", methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = get_user(username, password)
        if user:
            session['id'] = user["id"]
            session['username'] = user["username"]
            res = make_response(
                dumps({"message": "User logged in"}, default=str))
            res.set_cookie('role', user["role"])
            return res
        else:
            error = "Invalid username or password"
            return dumps({"error": error}, default=str), 401


@app.route("/logout/")
def logout():
    session.clear()
    res = make_response(redirect(url_for('home')))
    res.set_cookie('role', 'guest')
    return res


@app.route("/comments/", methods=['GET', 'POST', 'PUT'])
def comments_route():
    if request.method == 'GET':
        commentList = {"comments": get_comments()}
        return dumps((commentList), default=str)
    if request.method == 'POST':
        author = session['username']
        text = request.get_json()['text']
        create_comment(author, text)
        return dumps({"author": author, "text": text}, default=str)
    elif request.method == 'PUT':
        id = request.get_json()['id']
        text = request.get_json()['text']
        update_comment(id, text)
        return dumps({"text": text}, default=str)


@app.route("/admin-panel/")
def admin_panel():
    role = "guest"
    if "id" in session:
        user = get_user_by_id(session['id'])
        if user:
            role = user["role"]
        return render_template("admin-panel.html", role=role, customers=get_customers())
    if "id" not in session:
        res = make_response(render_template("admin-panel.html", role=role))
        res.set_cookie('role', 'guest')
        return res


@app.route("/create-user/", methods=['GET', 'POST'])
def admin_create_user():
    if request.method == 'GET':
        return render_template("admin-panel.html", id=id)
    elif request.method == 'POST':
        username = request.get_json()['username']
        password = request.get_json()['password']
        new_user_role = request.get_json()['role']
        logged_user_role = request.cookies.get('role')
        if logged_user_role == "admin":
            user = get_user_by_username(username)
            if user:
                error = "User already exists"
                return dumps({"error": error}, default=str), 403
            else:
                create_user(username, password, new_user_role)
                return dumps({"message": "User created"}, default=str)
        else:
            error = "Only admin can create users"
            return dumps({"error": error}, default=str), 403


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


@app.route('/robots.txt')
def static_from_root():
    return send_from_directory("", "robots.txt")


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)
