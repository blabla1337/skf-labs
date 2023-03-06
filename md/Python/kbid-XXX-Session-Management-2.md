# KBID XXX - Session Management - Part 2

## Running the app

```
$ sudo docker pull blabla1337/owasp-skf-lab:Session-Management-2
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:Session-Management-2
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Running the app Python3

First, make sure python3 and pip are installed on your host machine. After installation, we go to the folder of the lab we want to practise "i.e /skf-labs/python/Session-Management-2/ " and run the following commands:

```
$ pip3 install -r requirements.txt
```

```
$ python3 <labname>
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

![Docker image and write-up thanks to @NtAlexio2 !](https://avatars.githubusercontent.com/u/110637492?v=4&size=200)

## Reconnaissance

One of the core components of any web-based application is the mechanism by which it controls and maintains the state for a user interacting with it. To avoid continuous authentication for each page of a website or service, web applications implement various mechanisms to store and validate credentials for a pre-determined timespan. These mechanisms are known as Session Management.

An attacker who is able to predict and forge a weak cookie can easily hijack the sessions of legitimate users.

Cookies are used to implement session management and are described in detail in RFC 2965. See [WSTG-SESS-01](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Session_Management_Testing/01-Testing_for_Session_Management_Schema) for more information.

The goal of this lab is to get access to administration panel, with normal user account. So let's start.

At the first look, there is default credentials and site leads us to perform new login:

![](../../.gitbook/assets/Session-Management-2-1.png)

Before performing new login, let's check if there is any cookie(s):

![](../../.gitbook/assets/Session-Management-2-2.png)

No cookies for now. so we just continue to login as user `john`:

![](../../.gitbook/assets/Session-Management-2-3.png)

New cookies! `SessionId` seems to be random and the `IsAdmin` looks really interesting. Before any manipulations, let's make sure how everything is look. The steps happened is here:
- We send a login request to `/login`
- We got new cookies (`SessionId` and `IsAdmin`)
- Server redirects us to `/panel`
- We are logged in as `john`, which seems it is a normal user account (`IsAdmin` equals 0 and there is no management options or something like)

![](../../.gitbook/assets/Session-Management-2-5.png)
![](../../.gitbook/assets/Session-Management-2-4.png)

In order to WSTG-SESS-01:
```
Tamper resistance: a cookie must resist malicious attempts of modification. If the tester receives a cookie like IsAdmin=No, it is trivial to modify it to get administrative rights, unless the application performs a double check (for instance, appending to the cookie an encrypted hash of its value)
```

## Exploitation

Let's start with our interesting cookie, found before: `IsAdmin`. Simply we change it from `0` to `1` and server:

![](../../.gitbook/assets/Session-Management-2-6.png)

Boom! we got administration panel. to make sure, we render page to check whats going on:

![](../../.gitbook/assets/Session-Management-2-7.png)

We successfully logged in as normal user `john` and we also able to manage website. Mission complete!

## Additional sources

{% embed url="https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/06-Session_Management_Testing/01-Testing_for_Session_Management_Schema" %}
