# Command Injection 4 - CMD-4

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-cmd4
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-cmd4
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

When we start the application we can see that there is a box where we can write an IP address in order to execute a ping against it.

![](../../.gitbook/assets/python/CMD-4/1.png)

First, we are going to try the functionality and execute the ping against the loopback address. We can also see the resulted output:

![](../../.gitbook/assets/python/CMD-4/2.png)

## Exploitation

For this lab we are going to try to make the website show us the result of a malicious command executed by the system unintentionally.
We start by trying methods like:

![](../../.gitbook/assets/python/CMD-4/3.png)

![](../../.gitbook/assets/python/CMD-4/4.png)

It seems that it may not be possible to execute OS commands taking advantage of the ping functionality. However, we suspect that maybe the website is
filtering some of these special characters usually used for command execution so we try some new:

![](../../.gitbook/assets/python/CMD-4/5.png)

We finally could execute a command (whoami)!!

Now we try with another simple example:

![](../../.gitbook/assets/python/CMD-4/6.png)

Goal achieved and filter bypassed!

## Additional sources

[https://www.owasp.org/index.php/Command_Injection](https://www.owasp.org/index.php/Command_Injection)
