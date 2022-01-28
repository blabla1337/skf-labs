# KBID XXX - Client Side Restriction Bypass

## Running the app nodeJs

First make sure nodejs and npm are installed on your host machine.
After installation, we go to the folder of the lab we want to practice.
"i.e /skf-labs/XSS, /skf-labs/RFI/" and run the following commands:

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

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/1.png)

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/2.png)

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/3.png)

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/4.png)

## Exploitation

![](../../.gitbook/assets/nodejs/Client-side-restriction-bypass/5.png)

And goal achieved! We could bypass the client-side restrictions.

## Additional sources

{% embed url="https://cwe.mitre.org/data/definitions/602.html" %}
