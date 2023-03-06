# import re
from flask import Flask, render_template, request, url_for, redirect, session
from json import dumps
from random import randint, choice


from db.db import seed_db
from db.users import get_user_by_id, get_user, create_user, get_user_by_username, get_all_user


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True
random_string = ''.join(
    [choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(20)])
app.secret_key = random_string


seed_db()


@app.route("/")
def home():
    username = None

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
            return dumps({"error": "Please fill all fields"}), 400
        user = get_user_by_username(username)
        if user:
            return dumps({"success": False, "error": "User already exists"}), 403
        else:
            create_user(username, password)
            return dumps({"success": True, "message": "User created", "username": username})


@app.route("/login/", methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        number1, number2, operator = generate_captcha()
        return render_template("login.html", number1=number1, number2=number2, operator=operator)
    elif request.method == 'POST':
        if "captcha" not in request.get_json() or "username" not in request.get_json() or "password" not in request.get_json():
            return dumps({"error": "Please fill all fields"}), 400
        username = request.get_json()['username']
        password = request.get_json()['password']
        captcha = request.get_json()['captcha']
        captcha = str(captcha)
        if username == "" or password == "" or captcha == "":
            return dumps({"error": "Please fill all fields"}), 400
        if check_int(captcha):
            captcha = int(captcha)
        else:
            return dumps({"error": "Incorrect captcha"}), 400
        if captcha not in valid_captchas:
            return dumps({"error": "Incorrect captcha"}), 400
        valid_captchas.remove(captcha)
        user = get_user(username, password)
        if user:
            session['id'] = user["id"]
            session['username'] = user["username"]
            return dumps({"message": "User logged in"}, default=str)
        else:
            error = "Invalid username or password"
            return dumps({"error": error}, default=str), 401


@app.route("/profile/")
def user_detail():
    if "id" in session:
        user = get_user_by_id(session['id'])
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('home'))


@app.route("/users/")
def users_route():
    users = get_all_user()
    return dumps(users, default=str)


@app.route("/users/<username>")
def user_route(username):
    user = get_user_by_username(username)
    if not user:
        return dumps(user, default=str), 404
    return dumps(user, default=str)


@app.route("/logout/")
def logout():
    session.clear()
    return redirect(url_for('home'))


valid_captchas = []


def generate_captcha():
   # random number from 1 to 100
    number1 = randint(1, 100)
    number2 = randint(1, 100)
    # random operator
    operator = choice(['+', '-', '*'])
    # calculate the result
    result = eval(f"({ number1 }) { operator } ({ number2 })")
    # store the result in a temporary list
    valid_captchas.append(result)
    return number1, number2, operator


def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()


@app.route("/captcha/")
def captcha():
    number1, number2, operator = generate_captcha()
    # return the captcha
    return dumps({"number1": number1, "number2": number2, "operator": operator}, default=str)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)
