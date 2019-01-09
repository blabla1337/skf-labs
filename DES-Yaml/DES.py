import pickle, sys, yaml
import urllib.request
#from StringIO import StringIO  # Python2
from io import StringIO  # Python3
from flask import Flask, request, url_for, render_template, redirect

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True


@app.route("/")
def start():
    return render_template("index.html")

@app.route("/information/&file=<path:filename>", methods=['GET'])
def deserialization(filename):
     print(filename, file=sys.stdout)
     if filename == 'file.yml':
         with open(filename, 'rb') as handle:
            if filename == 'file.yml':
                # Import the PyYAML dependency
                with open(filename) as yaml_file:
                # Unsafely deserialize the contents of the YAML file
                    content = yaml.load(yaml_file)
     else:
         response = urllib.request.urlopen(filename)
         res = response.read()
         text_file = open("hacker_input.txt", "wb")
         attack = str(res)
         text_file.write(res)
         text_file.close()
         with open("hacker_input.txt") as yaml_file:
         # Unsafely deserialize the contents of the YAML file
             content = yaml.load(yaml_file)

     return render_template("index.html", content = content["foo"])

if __name__ == "__main__":
    app.run(host='0.0.0.0')
	
 
