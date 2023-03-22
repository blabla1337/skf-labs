# Auth-Bypass-1

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:auth-bypass-1
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:auth-bypass-1
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

While most applications require authentication to gain access to private information or to execute tasks, not every authentication method is able to provide adequate security. Negligence, ignorance, or simple understatement of security threats often result in authentication schemes that can be bypassed by simply skipping the log in page and directly calling an internal page that is supposed to be accessed only after authentication has been performed.

In addition, it is often possible to bypass authentication measures by tampering with requests and tricking the application into thinking that the user is already authenticated. This can be accomplished either by modifying the given URL parameter, by manipulating the form, or by counterfeiting sessions.

Obviously, an attacker can tamper with the URL, the form or the session cookie in order to get logged in as a user without knowing the actual credentials.

The goal of this lab is to get logged in as an administrator without knowing his/her credentials

Lets start the application and register a new user

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/1.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/2.png)

Now that we have valid credentials, we can login:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/3.png)

## Exploitation

We can capture the login in the burpsuite proxy and send it to the repeater. We notice that with every login, the session cookie stays the same. It is high likely that this sessionid is related to our user name:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/4.png)

If we quickly google for this sessionid, we find that the sessionID seems to be corresponding to 'user':

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/5.png)

We can check try to identify the hash:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/6.png)

it seems to be a sha1...

Ok, let's lookup the hash of 'admin':

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/7.png)

\-> D033E22AE348AEB5660FC2140AEC35850C4DA997

Now we can set our sessionID to the sha1 hash of admin:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/8.png)

Click 'proceed' to go to the authenticated section of the application:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-1/9.png)

## Additional sources

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html" %}
