from flask import Flask, request, url_for, render_template, redirect
import requests
import socket
import re
from subprocess import Popen

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

Popen("cd /tmp; echo \"Congratulations!\" > secret.txt; python3 -m http.server -b 127.0.0.1 80", shell=True)

@app.route("/")
def start():
    return render_template("index.html")


@app.route("/rebind", methods=['GET'])
def rebind():

    if((str(request.args.get('hostname')).lower() == "localhost".lower() or str(request.args.get('hostname') == "127.0.0.1") and not re.search('[A-Za-z]+', str(request.args.get('hostname'))))):
        return render_template("index.html", read = "'localhost' and '127.0.0.1' are filtered but... (un)luckily the DNS resolution is performed afterwards this filter.")
    else:
        try:
            if (socket.gethostbyname(request.args.get('hostname')) == "127.0.0.1"): # just to prevent SSRF against other websites
                return render_template("index.html", read = requests.get("http://" + request.args.get('hostname')).text)
            else:
                return render_template("index.html", read = "Only loopback requests are allowed here.")
        except:
    	        return render_template("index.html", read = "The service to access is listening on localhost (port 80). For DNS rebinding attacks you are expected to control the DNS resolution. </br>For such purpose, you have to setup an authoritative DNS for one of your domains... or use one already <a href=\"https://github.com/brannondorsey/whonow\">available</a>.")

    return render_template("index.html", read = "The service to access is listening on localhost (port 80). For DNS rebinding attacks you are expected to control the DNS resolution. </br>For such purpose, you have to setup an authoritative DNS for one of your domains... or use one already <a href=\"https://github.com/brannondorsey/whonow\">available</a>.")

if __name__ == "__main__":
    app.run(host='0.0.0.0')

	



