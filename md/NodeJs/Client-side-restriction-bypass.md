# Client Side Restriction Bypass

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-client-side-restriction-bypass
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-client-side-restriction-bypass
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The app allows us to select a number between 3 and 13 from the number input form. Let's also try typing numbers outside that interval directly into the field.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/1.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/2.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/3.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/4.png)

## Exploitation

We could intercept and modify the request on Burp:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/5.png)

Or alternatively, use devtools to modify the client-side restrictions directly:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/6.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Client-Side-Restriction-Bypass/7.png)

And goal achieved! We could bypass the client-side restrictions.

## Additional sources

{% embed url="https://cwe.mitre.org/data/definitions/602.html" %}
