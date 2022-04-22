# NodeJS - CSS Injection (CSSI)

## Running the app nodeJs

First make sure nodejs and npm are installed on your host machine. After installation, we go to the folder of the lab we want to practice. "i.e /skf-labs/XSS, /skf-labs/RFI/" and run the following commands:

```
$ npm install
```

```
$ npm start
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

When we start the application we can see that there is a text box that allow you to write a color name.

![](../../.gitbook/assets/java/CSSI/1.png)

We can write a color like:

![](../../.gitbook/assets/java/CSSI/2.png)

And depending on the color that we chose, this will be the color in the text below:

![](../../.gitbook/assets/java/CSSI/3.png)

## Exploitation

If we check how the text that we wrote in the text box is later put into the code we can see:

![](../../.gitbook/assets/java/CSSI/4.png)

If we try to insert a malicious code that we know it will be inserted in the source code, we can try something like this:

```
blue;}</style><script>alert("CSSI")</script>
```

![](../../.gitbook/assets/java/CSSI/5.png)

This code should show an alert box or pop up alerting the text "CSSI". If we check the website after sending the malicious request:

![](../../.gitbook/assets/java/CSSI/6.png)

And goal achieved!

## Additional sources

{% embed url="https://www.owasp.org/index.php/Testing_for_CSS_Injection_(OTG-CLIENT-005)" %}
