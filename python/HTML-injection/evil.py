#!/usr/bin/env python3

from flask import Flask, render_template, json

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/logger/<log>")
def logger(log):
    print("--------------------")
    print(log)
    print("--------------------")
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
