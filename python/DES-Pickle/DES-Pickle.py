import pickle, sys, yaml
from io import StringIO  # Python3
from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
        user = {'name': 'ZeroCool'}
        with open('filename.pickle', 'wb') as handle:
            pickle.dump(user, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('filename.pickle', 'rb') as handle:
            a = pickle.load(handle)
        return render_template("index.html", content = a)


@app.route("/sync", methods=['POST'])
def deserialization():
        with open("pickle.hacker", "wb+") as file:
            att = request.form['data_obj']
            attack = bytes.fromhex(att)
            file.write(attack)
            file.close()
        with open('pickle.hacker', 'rb') as handle:
            a = pickle.load(handle)
            print(attack)
            return render_template("index.html", content = a)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')

