from flask import Flask, request, url_for, render_template, redirect
import requests, validators, os

app = Flask(__name__, static_url_path = '/static', static_folder = 'static')
app.config['DEBUG'] = True
os.system("bash run_services.sh")

@app.route("/")
def start():
    return render_template("index.html")

@app.route("/check_existence", methods = ['POST'])
def ssrf():
    url = request.form['url']

    if not validators.url(url):
        return render_template("index.html", result = "Target resource is not reacheable.") 

    try:
        requests.head(url, timeout=2.000)
        return render_template("index.html", result = "Webpage found!")
    except Exception as e:
        if "NewConnectionError" in str(e):
            return render_template("index.html", result = "Target resource is not reacheable.") 
        else:
            return render_template("index.html", result = "Target resource is reacheable!")
    
if __name__ == "__main__":
  app.run(host = '0.0.0.0')
