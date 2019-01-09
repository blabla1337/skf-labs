from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect, make_response, request, session


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True


# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'
app.config.update(dict(
    SECRET_KEY= "woopie",
    SESSION_COOKIE_HTTPONLY = True
))


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli  = Classes()
    values = sqli.getUser(request.form['username'])
    if values:
        if values[0][2] == request.form['password']:
            session['userId'] = values[0][0]
            session['loggedin'] = True
            pref = sqli.getColor(values[0][0])
            color = pref[0][0]
            return render_template("loggedin.html", color = color)       
    return render_template("index.html")
    
    
@app.route("/update", methods=['POST', 'GET'])
def update():
    if not session.get('loggedin'):
        return render_template('index.html')
    sqli  = Classes()
    if request.method == "POST":
        sqli.updateColor(request.form['color'], session.get('userId'))
    
    pref = sqli.getColor(session.get('userId'))
    color = pref[0][0]
    return render_template("loggedin.html", color = color)
        
    
if __name__ == "__main__":
    app.run()
	

