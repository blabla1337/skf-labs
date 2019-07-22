from flask import Flask, request, url_for, render_template, redirect
import os
import subprocess
import time


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/", methods=['GET'])
def start():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def home():
    sleepingtime = int(request.form['numero'])
    print("You sleep " + str(sleepingtime) + " hours a day")

    if sleepingtime < 7 and sleepingtime >= 3:
        output = "You should sleep more"
    elif sleepingtime >= 7 and sleepingtime <= 9:
        output = "You sleep a proper while"
    elif sleepingtime > 9 and sleepingtime <= 13:
        output = "You should sleep less"
    elif sleepingtime == 2 or (sleepingtime > 13 and sleepingtime < 24):
        output = "OMG!"
    else:
        output = "That's not possible... HACKER!"

    return render_template("index.html", read = output)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
