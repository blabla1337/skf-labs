from xml.dom.pulldom import START_ELEMENT, parseString
import xml
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return render_template("index.html")


@app.route("/home", methods=['POST', 'GET'])
def xxe():
    doc = parseString(request.form['xxe'])
    try:
        for event, node in doc:
            if event == START_ELEMENT and node.localName == "items":
                doc.expandNode(node)
                nodes = node.toxml()
        return render_template("index.html", nodes=nodes)
    except (UnboundLocalError, xml.sax._exceptions.SAXParseException):
        return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
