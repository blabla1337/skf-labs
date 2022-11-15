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

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/1.png)

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/2.png)

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/3.png)

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/4.png)

## Exploitation

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/5.png)

And goal achieved! We could bypass the client-side restrictions.

## Additional sources

{% embed url="https://cwe.mitre.org/data/definitions/602.html" %}
