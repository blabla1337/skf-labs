# KBID 3 - Cross Site Scripting

## Running the app Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:xss
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:xss
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Running the app Python3

First, make sure python3 and pip are installed on your host machine. After installation, we go to the folder of the lab we want to practise "i.e /skf-labs/XSS/, /skf-labs/jwt-secret/ " and run the following commands:

```
$ pip3 install -r requirements.txt
```

```
$ python3 <labname>
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

![Docker image and write-up thanks to DefDev!](.gitbook/assets/logo.defdev.1608z.whtonblk.256.png)

## Reconnaissance

### Step 1

The application shows an input field box were we can try our injections. Lets first inject a normal test string and see how our input is used in the application.

![](.gitbook/assets/screen-shot-2019-01-29-at-12.58.36.png)

As you can see below the request in our intercepting proxy that was made by the application.

![](.gitbook/assets/screen-shot-2019-01-29-at-13.01.50.png)

In the source of the application we can see that this application will take the user input and use a template variable to display it in the application.

```python
@app.route("/home", methods=['POST'])
def home():
    xss = request.form['string']
    return render_template("index.html",xss = xss)
```

```markup
<center> <p style="font-size:2em;">{% autoescape false %}{{xss}}{% endautoescape %}</p></center>
```

The variable is then used in the index.html to display the content suplied by the user. But as you can see the autoescape method is set to false. This indicates that is should be possible to perform a Cross Site Scripting (XSS) injection.

## Exploitation

### Step 1

Now we have seen where the user input is being reflected in the application we will have to look what dangerous HTML characters are not properly escaped so we can build our XSS payload. So for our first check we use the following string as an input:

```
foobar"></
```

![](.gitbook/assets/screen-shot-2019-01-29-at-13.02.25.png)

As you can see the application did not encode or blacklisted any of the dangerous HTML characters. Now lets try the XSS payload to see if this also is reflected back withouth any escaping or blacklist filtering.

```
foobar"><script>alert(123)</script>
```

![](.gitbook/assets/screen-shot-2019-01-29-at-13.03.01.png)

Again the application is not encoding or blacklisted any of the dangerous HTML characters. This payload seems to work in the intercepting proxy. Now lets try it in our Chrome browser.

![](.gitbook/assets/screen-shot-2019-01-29-at-13.08.38.png)

As you can see in Chrome it didn't work because of the XSS Auditor setting that is enforced. This is an special browser header that can be set do add an additinal layer of security to the application. Let's use Firefox to see if we are able to trigger the XSS with our payload there.

![](.gitbook/assets/screen-shot-2019-01-29-at-13.05.36.png)

In Firefox we can see the XSS alert pop-up and we have successfully performed the XSS attack.

## Additional sources

Please refer to the OWASP testing guide for a full complete description about path traversal with all the edge cases over different platforms!

{% embed url="https://www.owasp.org/index.php/Testing_for_Reflected_Cross_site_scripting_(OTG-INPVAL-001)" %}
