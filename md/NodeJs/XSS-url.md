# Cross site scripting \(href\)

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-xss-url
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-xss-url
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

### Step 1

The application invites you to fill a website in the input box, that will be used from the "visit my website!" link to redirect to it.

![](../../.gitbook/assets/nodejs/XSS-url/1.png)

If we insert `https://google.com`, and click on "visit my website!" we will be redirected to the Google website. As we can see in the screenshot below our input is reflected in the page inside an `href` attribute.

![](../../.gitbook/assets/nodejs/XSS-url/2.png)

#### Step 2

The next step is to see if we could include JavaScript that can be executed in the `href` attribute.

href="javascript:JS PAYLOAD"

Autoescape is disabled by default so every characters will be reflected in the following snippet in the template.

```markup
 <center> <p style="font-size:2em;"><a style="font-size:20px;" href="<%- xss %>">visit my website!</a></p></center>
```

## Exploitation

#### Step 1

Now we have seen where the user input is being reflected in the href, we can craft the payload to trigger an alert box and exploit our XSS.

```markup
javascript:alert('XSS')
```

and clicking the button, we achieve what we were looking for.

![](../../.gitbook/assets/nodejs/XSS-url/3.png)

## Additional sources

Please refer to the OWASP testing guide for a full complete description about cross site scripting!

{% embed url="https://owasp.org/www-community/attacks/XSS-url/" %}
{% embed url="https://ejs.co/#docs" %}
