from flask import Flask, request, url_for, render_template, session, redirect
import sqlite3

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


def valid_login(username, password):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * from emptbl where username=? and password=?', (username, password))
    result = cur.fetchone()
    if result is not None:
        session["username"] = result[1]
    if result is not None:
        return True
    else:
        return False


def log_the_user_in(username):
    return render_template('dashboard.html', username=username)


@app.route("/")
@app.route("/login", methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            session["log"] = True
            return log_the_user_in(request.form['username'])
        else:
            error = 'invalid username/password'
        return render_template("index.html", error=error)
    else:
        error = None

    return render_template('index.html', error=error)


def valid_login_forgot(username):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * from emptbl where username=?', (username,))
    result = cur.fetchone()
    if result is not None:
        session["username"] = result[1]
    if result is not None:
        return True
    else:
        return False


@app.route("/forgot", methods=['POST', 'GET'])
def forgot():
    error = None
    if request.method == 'POST':
        if valid_login_forgot(request.form['username']):
            session["log"] = True
            error = 'if your username is valid you will recivee an email with password'
            #return log_the_user_in(request.form['username'])
            return render_template("forgot.html", error=error)
        else:
            error = 'invalid username'
            return render_template("forgot.html", error=error)
    else:
        error = None
    return render_template('forgot.html', error=error)


@app.route("/dashboard", methods=['POST', 'GET'])
def dashboard():
    if not session.get('log'):
        return render_template('index.html')
    else:
        if valid_login_forgot(session.get('username')):
            error = None
            return log_the_user_in(session.get('username'))
        else:
            return render_template("forgot.html")
    return render_template("dashboard.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.secret_key = "123456abcd"
    app.run(debug=True)
