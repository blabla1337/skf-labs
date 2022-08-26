import base64
from models.sqlimodel import *
from time import gmtime, strftime
from flask import Flask, render_template


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True

@app.route("/")
def start():
    time = strftime("%H:%M", gmtime())
    csrf = "admin" + time
    csrf_raw = base64.b64encode(csrf.encode())
    csrf_token = str(csrf_raw, 'utf-8')
    return render_template("evil.html", csrf_token = csrf_token)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
	

