# Python - Client Side Restriction Bypass

## Running the app

```
$ sudo docker pull blabla1337/owasp-skf-lab:client-side-restriction-bypass
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:client-side-restriction-bypass
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Running the app Python3

First, make sure python3 and pip are installed on your host machine. After installation, we go to the folder of the lab we want to practise "i.e /skf-labs/XSS/, /skf-labs/jwt-secret/ " and run the following commands:

```
$ pip3 install -r requirements.txt
```

```
$ python3 <labname>
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

![Docker image and write-up thanks to Contrahack.io !](<../../.gitbook/assets/ing\_primary\_logo (2).png>)

## Reconnaissance

![](../../.gitbook/assets/CSRB-10.png)

![](../../.gitbook/assets/CSRB-11.png)

![](../../.gitbook/assets/CSRB-12.png)

![](../../.gitbook/assets/CSRB-13.png)

## Exploitation

![](../../.gitbook/assets/CSRB-14.png)

And goal achieved! We could bypass the client-side restrictions.

## Additional sources
