# import re
from flask import Flask, render_template, request, url_for, redirect, session
from json import dumps


from db.db import seed_db
from db.users import get_user_by_id, get_user, create_user, get_user_by_username, get_all_user, generate_username, check_email


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True
app.secret_key = 'mysecret'


seed_db()


@app.route("/")
def home():
    username = None

    # if "id" in session:
    #     user = get_user_by_id(session['id'])
    #     if user is None:
    #         session.clear()
    #         redirect(url_for('home'))

    if "username" in session:
        username = session['username']

    return render_template("index.html", user=username)


@app.route("/register/", methods=['GET', 'POST'])
def register_route():
    if request.method == 'GET':
        return render_template("register.html")
    elif request.method == 'POST':
        name = request.get_json()['name']
        lastname = request.get_json()['lastname']
        password = request.get_json()['password']
        address = request.get_json()['address']
        phone = request.get_json()['phone']
        email = request.get_json()['email']
        if name == "" or lastname == "" or password == "" or address == "" or phone == "" or email == "":
            return dumps({"error": "Please fill all fields"}), 400

        username = generate_username(name, lastname)

        emailExists = check_email(email)
        if emailExists:
            return dumps({"success": False, "error": "Email already exists"}), 403
        else:
            create_user(name, lastname, username,
                        password, address, phone, email)
            return dumps({"success": True, "message": "User created", "username": username})


@app.route("/login/", methods=['GET', 'POST'])
def login_route():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.get_json()['email']
        password = request.get_json()['password']
        user = get_user(email, password)
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', use_reloader=False)
