from flask import Flask, request, url_for, render_template, redirect, make_response
import requests


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/allowed", methods=['GET'])
def allowed():
    content = requests.get('http://0.0.0.0:5000/allowed').content
    return render_template('index.html', content = content)

@app.route("/protected", methods=['GET'])
def protected():
    content = requests.get('http://0.0.0.0:5000/protected').content
    return render_template('index.html', content = content)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
