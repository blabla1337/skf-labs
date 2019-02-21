from flask import Flask, request, url_for, render_template, redirect
import requests, validators
import re

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')
app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/verify_email", methods = ['POST'])
def regex():
    email = request.form['email']
    match = re.search(r"^([0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*@{1}([0-9a-zA-Z][-\w]*[0-9a-zA-Z]\.)+[a-zA-Z]{2,9})$", str(email))

    if (match):
        return render_template("index.html", result = "Matched!")
    else:
        return render_template("index.html", result = "Not matched!")
    
   
if __name__ == "__main__":
  app.run(host = '0.0.0.0')
