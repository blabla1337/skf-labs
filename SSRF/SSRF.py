from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def ssrf():
    url = request.form['url']
    try:
    r = requests.get(url)
    except requests.exceptions.RequestException as e:
	if "refused" in str(e):
	    result = "Target not reacheable."
        else
	    result = "Target resource is reacheable!"
	
    result = "Webpage found."

    return render_template("index.html", result = result)



if __name__ == "__main__":
    app.run(host='0.0.0.0')
	


