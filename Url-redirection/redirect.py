from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html", content = "Sorry, this is the old website.")

@app.route("/redirect", methods=['POST', 'GET'])
def redirector():
    landing_page = request.args.get('newurl')
    return redirect(landing_page, 302)

@app.route("/newsite")
def newsite():
    return render_template("index.html", content = "Welcome to the new website!")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
