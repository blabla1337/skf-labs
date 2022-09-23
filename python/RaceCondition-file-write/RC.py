#!/usr/bin/env python3

from flask import Flask, render_template, send_file, make_response

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/<string:value>", methods=['GET'])
def home(value):
    # Create a Python file object using open() and the with statement
    with open("shared-file.txt", 'w') as f:
        f.write(value)
        f.closed
        f.closed
    file = open("shared-file.txt", "r") 
    response = make_response(send_file("shared-file.txt", attachment_filename="shared-file.txt"))
    response.headers.set("Content-Type", "text/html; charset=utf-8")
    response.headers.set("Content-Disposition", "attachment; filename=shared-file.txt")
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

