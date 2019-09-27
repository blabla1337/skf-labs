from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect, make_response, request
import hashlib


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True 


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
        sqli  = dbaccess()
        values=sqli.getUser(request.form['username'])
        if values:
            msg="Find the way to login as an admin !"
            username=values[0][0]
            if values[0][1] == request.form['password']:
                res = make_response(render_template("loggedin.html",username=username),msg=msg)
                res.set_cookie("sessionid", hashlib.sha1(username.encode('utf-8')+'SKFowaspLabs'.encode('utf-8')).hexdigest())
                return res
            else:
                return render_template("index.html")
        return render_template("index.html")
        
()
@app.route("/register", methods=['POST', 'GET'])
def register():
    return render_template("register.html",renderlogout=isloggedin())

@app.route("/loggedin", methods=['GET'])
def loggedin():
    txt='You have to login first'
    msg="Find the way to login as an admin !"
    if isloggedin():
        hash=request.cookies.get('sessionid')
        sqli  = dbaccess()
        values=sqli.getHash(hash.lower())
        username=values[0][0].lower()
        if username == 'admin':
            msg="Congratulations !"
        return render_template("loggedin.html",username=username,msg=msg)
    else:       
        return render_template("index.html",msg=txt)

@app.route("/about", methods=['GET'])
def about():
    return render_template("about.html")  

def isloggedin():
    if 'sessionid' in request.cookies:
        hash=request.cookies.get('sessionid')
        sqli  = dbaccess()
        values=sqli.getHash(hash.lower())
        if values:
            return True
    return False


@app.route("/create", methods=['POST'])
def create():
    usr=request.form['username'].strip().lower()
    pwd=request.form['password'].strip()
    if usr != '' and pwd !='':
        sqli  = dbaccess()
        txt=''
        values=sqli.getUser(usr)
        if values:
            #user exists, update password, except for admin
            username=values[0][0].lower()
            if username != 'admin':
                sqli.updatePassword(usr,pwd)
                txt='Your password has been updated'
            else:
                txt='Nice try ! ;-)'
                return render_template("register.html",msg=txt)
        else:
            #new user
            sqli.CreateUser(usr,pwd)
            txt='Your user has been created'
        return render_template('index.html',msg=txt)
    else:
        txt='Blank username and/or password are not allowed'
        return render_template('register.html',msg=txt) 

@app.route("/logout", methods=['GET'])
def logout():
    txt=''
    if request.method == "GET":
        txt='You successfully logged out'
        res = make_response(render_template('index.html',msg=txt))
        res.set_cookie('sessionid', '', expires=0)
        return res
    txt="You are not logged out"
    return render_template('index.html',msg=txt)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
