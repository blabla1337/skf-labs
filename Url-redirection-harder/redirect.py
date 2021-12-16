from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


def blacklist(url):
    blacklist = ["."]
    for b in blacklist:
        if url.find(b) != -1:
            return True
    return False


@app.route("/")
def start():
    return render_template("index.html", content = "Sorry, this is the old website.")


@app.route("/redirect", methods=['POST', 'GET'])
def redirector():
    landing_page = request.args.get('newurl')
    if blacklist(landing_page):
        return render_template("index.html", content = "Sorry, you cannot use \".\" in the redirect")
    return redirect(landing_page, 302)


@app.route("/newsite")
def newsite():
    return render_template("index.html", content = "Welcome to the new website!")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

