# Content Security Policy - CSP

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:js-csp
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:js-csp
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The main use of the content security policy header is to, detect, report, and reject XSS attacks. The core issue in relation to XSS attacks is the browser's inability to distinguish between a script that's intended to be part of your application, and a script that's been maliciously injected by a third-party. With the use of CSP\(Content Security policy\), we can tell the browser which script is safe to execute and which scripts are most likely been injected by an attacker.

![](../../.gitbook/assets/python/CSP/1.png)

## Exploitation

In the first scenario we explore the execution of an XSS attack without CSP in place.

![](../../.gitbook/assets/python/CSP/2.png)

![](../../.gitbook/assets/python/CSP/3.png)

With CSP in place, when we try to perform a XSS attack we notice that CSP header block the scripts since the inclusion of inline scripts is not permitted.

![](../../.gitbook/assets/python/CSP/4.png)

![](../../.gitbook/assets/python/CSP/5.png)

## Additional sources

{% embed url="https://owasp.org/www-community/controls/Content_Security_Policy" %}
