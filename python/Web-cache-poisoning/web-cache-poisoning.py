from flask import Flask, render_template, request, make_response
from flask_caching import Cache


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config.from_object('config.Config')

cache = Cache(app)

EXPLOIT_SERVER = app.config['ATTACK_SERVER_URL']


@app.route("/", defaults={'url': ""})
@app.route("/<path:url>")
def start(url):
    forwarded_host = request.headers.get('X-Forwarded-Host', '')
    if forwarded_host:
        request.host = forwarded_host

    response = cache.get(request.full_path)
    if response is not None and request.headers.get('Cache-Control', '') != 'no-cache':
        response.headers.set('X-Cache', 'hit')
    else:
        response = make_response(
            render_template('index.html', 
            tracker_site=request.host,
            exploit_server=EXPLOIT_SERVER))
        response.headers.set('X-Cache', 'miss')
        cache.set(request.full_path, response)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
