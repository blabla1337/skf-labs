#!/usr/bin/env python3

from flask import Flask, request, url_for, render_template, redirect
import ssl

# Sauce:
# https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
# https://werkzeug.palletsprojects.com/en/1.0.x/serving/
# https://docs.python.org/2/library/ssl.html

# Safest
# This still allows TLS re-negoation, but offers none besides TLSv1_2.
# Solutions: upgrade to Python >= 3.7 and OpenSSL >= 1.1.0.
#ctx = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

# Safer
#ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
#ctx.options |= ssl.OP_NO_SSLv2
#ctx.options |= ssl.OP_NO_SSLv3

# Unsafe
ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv3)

ctx.load_cert_chain('/ssl.cert', '/ssl.key')

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("index.html")


#@app.route("/home", methods=['POST'])
#def home():
#    xss = request.form['string']
#    return render_template("index.html",xss = xss)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0',ssl_context='adhoc',ssl_version='ssl.PROTOCOL_TLSv1')
    app.run(debug=True,host='0.0.0.0',ssl_context=ctx)

