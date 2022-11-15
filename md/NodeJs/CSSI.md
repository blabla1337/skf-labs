# CSS Injection - CSSI

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-cssi
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-cssi
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

When we start the application we can see that there is a text box that allow you to write a color name.

![](../../.gitbook/assets/nodejs/CSSI/1.png)

We can write a color like:

![](../../.gitbook/assets/nodejs/CSSI/2.png)

And depending on the color that we chose, this will be the color in the text below:

![](../../.gitbook/assets/nodejs/CSSI/3.png)

## Exploitation

If we check how the text that we wrote in the text box is later put into the code we can see:

![](../../.gitbook/assets/nodejs/CSSI/4.png)

If we try to insert a malicious code that we know it will be inserted in the source code, we can try something like this:

```text
blue;}</style><script>alert("CSSI")</script>
```

![](../../.gitbook/assets/nodejs/CSSI/6.png)

This code should show an alert box or pop up alerting the text "CSSI".
If we check the website after sending the malicious request:

![](../../.gitbook/assets/nodejs/CSSI/5.png)

And goal achieved!

## Additional sources

{% embed url="https://www.owasp.org/index.php/Testing_for_CSS_Injection_(OTG-CLIENT-005)" %}
