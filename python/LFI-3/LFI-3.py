from flask import Flask, request, render_template, current_app
import os, urllib


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = False

@app.route("/")
def start():
    return render_template("index.html")


@app.route("/home", methods=['POST'])
def home():
    filename = urllib.parse.unquote(request.form['filename'])
    read='try harder...'
    if '../' not in filename:
        filename = urllib.parse.unquote(filename)
        if os.path.isfile(current_app.root_path + '/'+ filename):
            with current_app.open_resource(filename) as f:
                read = f.read()
    return render_template("index.html",read = read)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

