from flask import Flask, request, url_for, render_template, redirect
import os
import subprocess
import time


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/home", methods=['POST'])
def home():
    text_input = request.form['text']
    os.system('echo Welcome ' + text_input + ' > /tmp/tmp.txt')

    f = open('/tmp/tmp.txt','r')
    text = f.read()

    return render_template("index.html", read = text)


if __name__ == "__main__":
    app.run(host='0.0.0.0')



