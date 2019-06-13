from flask import Flask, request, url_for, render_template, redirect
import os
import subprocess
import time


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def start():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def home():
    text_input = request.form['text']
    os.system('echo ' + text_input + ' >> welcome')
    text = "WELCOME!"

    return render_template("index.html", read = text)


if __name__ == "__main__":
    app.run(host='0.0.0.0')



