from flask import Flask, request, url_for, render_template, redirect, send_file

app = Flask(__name__)
app.config['DEBUG'] = True


@app.route('/<path:path>')
def static_file(path):
    return send_file(path)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0', port=8081)

