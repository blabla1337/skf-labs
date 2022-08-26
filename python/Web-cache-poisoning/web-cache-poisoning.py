from flask import Flask, render_template
from flask_caching import Cache


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object('config.Config')

cache = Cache(app)


@app.route("/")
@cache.cached(timeout=30)
def start():
    return render_template("index.html", exploit_server=app.config['ATTACK_SERVER_URL'])


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
