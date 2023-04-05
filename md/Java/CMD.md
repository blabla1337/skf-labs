# Command Injection - CMD

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:java-cmd
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:java-cmd
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The command injecion is an attack in which the goal is execution of
arbitrary commands on the host operating system via a vulnerable
application. Command injection attacks are possible when an application
passes unsafe user supplied data (forms, cookies, HTTP headers etc.) to
a system shell. In the first step, the attacker needs to inspect the
functioning of the web app in order to find possible injection points.
When we start the application we can see that there is an image and the option to resize the image.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/CMD/1.png)

Now, we are going to select a value and press the button.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CMD/1.png)

If we inspect the request with an intercepting proxy \(we are using
Burp\) we can see that the application is performing a POST request to
/home. In the request we send the number (in percentage) to resize the image.
In the response, we can check that the image has been resized.

## Exploitation

Let's try to get remote code execution.

Intercepting the request on burp, we can try to pipe other commands, like opening the calculator on linux (xcalc) as PoC.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CMD/2.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/CMD/3.png)

Bingo! 

## Additional sources

{% embed url="https://owasp.org/www-community/attacks/Command_Injection" %}

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html" %}
