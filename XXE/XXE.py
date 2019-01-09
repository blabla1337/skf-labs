from flask import Flask, request, url_for, render_template, redirect
from xml.dom import minidom

from xml.dom.pulldom import START_ELEMENT, parseString


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/home", methods=['POST', 'GET'])
def xxe():
    doc = parseString(request.form['xxe'])
    for event, node in doc:
        if event == START_ELEMENT and node.localName == "items":
            doc.expandNode(node)
            nodes = node.toxml()
    return render_template("index.html", nodes = nodes)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
	


