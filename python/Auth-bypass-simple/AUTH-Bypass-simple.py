from models.sqlimodel import *
from flask import Flask, request, render_template, make_response, request, session


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True


# Load default config and override config from an environment variable
# You can also replace password with static password:  PASSWORD='pass!@#example'
app.config.update(dict(
    SECRET_KEY= "e5ac-4ebf-03e5-9e29-a3f562e10b22",
    SESSION_COOKIE_HTTPONLY = True
))


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli  = Classes()
    if request.method == "POST":
        values = sqli.getUser(request.form['username'])
        if values:
            if values[0][2] == request.form['password']:
                session['loggedin'] = True
                pref = sqli.getApi(values[0][0])
                api = pref[0][0]
                resp = make_response(render_template("loggedin.html", api = api))
                resp.set_cookie('userId', '1')
                return resp
        return render_template("index.html")
    else:
        pref = sqli.getApi(request.cookies.get('userId'))
        api = pref[0][0]
        return render_template("loggedin.html", api = api)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
