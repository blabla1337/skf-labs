from flask import Flask, request, url_for, render_template, redirect
from subprocess import call


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():

    return render_template("index.html")


@app.route("/home", methods=['POST'])
def home():
    injection = request.form['inj_text']
    return render_template("index.html", injection=injection)

if __name__ == "__main__":
    app.run(host='0.0.0.0')


