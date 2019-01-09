from flask import Flask, request, url_for, render_template, redirect, make_response
import json


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")


@app.route("/unprotected", methods=['POST'])
def unprotected():
    val = request.form['no_header']
    xss = json.dumps({"key": val , "key2": "another value"}, sort_keys=True)
    return render_template("index.html", xss = xss)


@app.route("/protected", methods=['POST'])
def protected():
    val = request.form['with_header']
    xss = json.dumps({"key": val, "key2": "another value"}, sort_keys=True)
    r = make_response(render_template('index.html', xss = xss))
    r.headers.set('Content-type', "application/json")
    return r
    
if __name__ == "__main__":
    app.run()
	

