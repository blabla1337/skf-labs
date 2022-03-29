# KBID 178 - Content-Security-Policy

## Running the app Java

First make sure java is installed on your host machine.
After installation, we go to the folder of the lab we want to practice.
"i.e /skf-labs/XSS, /skf-labs/RFI/" and run the following command:

```
$ ./mvnw spring-boot:run
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

The main use of the content security policy header is to, detect, report, and reject XSS attacks. The core issue in relation to XSS attacks is the browser's inability to distinguish between a script that's intended to be part of your application, and a script that's been maliciously injected by a third-party. With the use of CSP\(Content Security policy\), we can tell the browser which script is safe to execute and which scripts are most likely been injected by an attacker.

## Exploitation

In the first scenario we explore the execution of an XSS attack without CSP in place.

![](../../.gitbook/assets/java/CSP/1.png)

![](../../.gitbook/assets/java/CSP/2.png)

With CSP in place, when we try to perform a XSS attack we notice that CSP header block the scripts since the inclusion of inline scripts is not permitted.

![](../../.gitbook/assets/java/CSP/3.png)

![](../../.gitbook/assets/java/CSP/4.png)

## Additional sources

{% embed url="https://owasp.org/www-community/controls/Content_Security_Policy" %}
