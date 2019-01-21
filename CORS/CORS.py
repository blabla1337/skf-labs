from models.sqlimodel import *
from flask import Flask, request, url_for, render_template, redirect, make_response, request, session
from flask_cors import CORS


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
            return redirect(url_for('xhr_get_info_stealing'))
    return render_template("index.html")


@app.route("/confidential", methods=['GET', 'POST'])
def xhr_get_info_stealing():
    if(session['loggedin']):
        response = make_response(render_template('loggedin.html'))
        response.headers.set("Access-Control-Allow-Credentials", "true")
    return response
        
    
if __name__ == "__main__":
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.run(host='0.0.0.0')
	

