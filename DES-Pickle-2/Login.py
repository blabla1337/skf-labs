from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect, make_response, request, session
import pickle, base64


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = False

# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'
app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = True
))

class usr:
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli  = Classes()
    if 'rememberme' in request.cookies:
        b64=request.cookies.get('rememberme')
        a = pickle.loads(base64.b64decode(b64))
        session['username'] = a.username
        session['loggedin'] = True
        return render_template("loggedin.html")
    else:
        values = 'admin' #
        values=sqli.getUser(request.form['username'])
        if values:
            if values[0][2] == request.form['password']:
                session['username'] = values[0][1]
                session['loggedin'] = True
                if 'rememberme' in request.form:
                    if request.form['rememberme'] == 'on':
                        u1 = usr(values[0][1],values[0][2])
                        ser = pickle.dumps(u1)
                        b64 = base64.b64encode(ser)
                        res = make_response(render_template("loggedin.html"))
                        res.set_cookie("rememberme", b64, 60*60*24*15)
                        return res
                else:
                    return render_template("loggedin.html")
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    return render_template("register.html")

@app.route("/create", methods=['POST'])
def create():
    sqli  = Classes()
    values=sqli.getUser(request.form['username'])
    if values:
        #user exists, update password
        sqli.updatePassword(request.form['username'],request.form['password'])
    else:
        #new user
        sqli.CreateUser(request.form['username'],request.form['password'])
    return render_template('index.html')

@app.route("/update", methods=['POST', 'GET'])
def update():
    if not session.get('loggedin'):
        return render_template('index.html')
    if request.method == "POST":
        if 'logout' in request.form['action'] :
            session['loggedin']= None
            res = make_response(render_template("index.html"))
            res.set_cookie('rememberme', '', expires=0)
            return res
        else:
            return render_template('index.html')
    else:
        return render_template('loggedin.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

