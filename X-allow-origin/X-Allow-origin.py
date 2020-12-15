# https://flask-cors.readthedocs.io/en/latest/

from flask import Flask, request, url_for, render_template_string, render_template, redirect, make_response
from flask.ext.cors import CORS, cross_origin


app = Flask(__name__, static_url_path='/static', static_folder='static')

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return response
    
app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/allowed", methods=['GET'])
@cross_origin()
def allowed():
    return "allowed"

@app.route("/protected", methods=['GET'])
def protected():
    return "protected"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

