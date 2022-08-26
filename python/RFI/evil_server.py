from flask import Flask, render_template


app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/evil.py")
def start():
    return render_template("evil.py")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
