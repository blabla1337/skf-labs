from models.sqlimodel import *
from flask import Flask, request, render_template, make_response, request
import hashlib


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = False 


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli = dbaccess()
    keys = request.form.keys()
    if 'username' in keys and 'password' in keys:
        try:
            username = request.form['username']
            password = request.form['password']
            values = sqli.validateUser(username, password) # Unsafe Function!
            if values:
                response = make_response(render_template("loggedin.html", username=values[0][0], msg="Congratulations!"))
                response.set_cookie("sessionid", hashlib.sha1(username.encode('utf-8')).hexdigest())
                return response
        except Exception as e:
            return render_template("500.html", error=str(e))
    return render_template("index.html")

@app.route("/loggedin", methods=['POST', 'GET'])
def loggedin():
    text = 'You have to login first'
    if isloggedin():
        hash = request.cookies.get('sessionid')
        sqli = dbaccess()
        values = sqli.getHash(hash.lower())
        username = values[0][0].lower()
        return render_template("loggedin.html", username=username, msg="Congratulations!")
    else:
        return render_template("index.html", msg=text)

def isloggedin():
    if 'sessionid' in request.cookies:
        hash = request.cookies.get('sessionid')
        sqli = dbaccess()
        values = sqli.getHash(hash.lower())
        if values:
            return True
    return False

@app.route("/logout", methods=['GET'])
def logout():
    text = ''
    if request.method == "GET":
        text = 'You successfully logged out'
        response = make_response(render_template('index.html',msg=text))
        response.set_cookie('sessionid', '', expires=0)
        return response
    text = "You are not logged out"
    return render_template('index.html', msg=text)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

