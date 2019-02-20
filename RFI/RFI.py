from flask import Flask, request, url_for, render_template, redirect
import datetime, requests, os, validators
from urllib.parse import urlparse

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/cmd", methods=['POST'])
def cmd():
    filename = request.form['filename']

    try:
        if "http" not in str(urlparse(filename).scheme):
        	filename = "http://127.0.0.1:5000/static/" + filename
        
        return render_template("index.html",result = eval(requests.get(filename).text))
    except Exception as e:
    	return render_template("index.html",result = "Unexpected error during the execution of the predefined command.")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
	
