from flask import Flask, request, url_for, render_template, redirect, make_response


app = Flask(__name__, static_url_path='/static', static_folder='../../static')

app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")


@app.route("/unprotected", methods=['POST'])
def unprotected():
    xss = request.form['no_csp']
    return render_template("index.html", xss = xss)


@app.route("/protected", methods=['POST'])
def protected():
    xss = request.form['with_csp']
    r = make_response(render_template('index.html', xss = xss))
    r.headers.set('Content-Security-Policy', "default-src 'self'")
    r.headers.set('Content-Security-Policy', "script-src 'http://127.0.0.1'")
    return r
    
if __name__ == "__main__":
    app.run()
	

