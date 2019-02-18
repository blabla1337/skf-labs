from flask import Flask, render_template, request, redirect
from io import StringIO  # Python3
import sys
import yaml
import base64

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return redirect("/information/eWFtbDogVGhlIGluZm9ybWF0aW9uIHBhZ2UgaXMgc3RpbGwgdW5kZXIgY29uc3RydWN0aW9uLCB1cGRhdGVzIGNvbWluZyBzb29uIQ==", code=302)

@app.route("/information/<input>", methods=['GET'])
def deserialization(input): 
    try: 
            if not input:
                return render_template("information/index.html")
            yaml_file = base64.b64decode(input)
            content = yaml.load(yaml_file)
    except:
            content = "The application was unable to  to deserialize the object!"
    return render_template("index.html", content = content['yaml'])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
	
