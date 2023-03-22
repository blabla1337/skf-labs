# Auth-Bypass-2

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:auth-bypass-2
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:auth-bypass-2
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

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/1.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/2.png)

Now that we have valid credentials, we can login:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/3.png)

## Exploitation

We can capture the login in the burpsuite proxy and send it to the repeater. We notice that with every login, the session cookie stays the same. It is high likely that this sessionid is related to our user name:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/4.png)

If we quickly google for this sessionid, we find nothing:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/5.png)

We can try to identify this hash:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/6.png)

It seems to be a sha1...

It is possible that the developer added a salt to the username and hashed the concatenated string admin+some_salt -> maybe this is also the reason why we can't find with Google what the hash represents.

The about page seem to contain a lot of text, maybe the salt is a typical word for this company that is also mentioned on that page…

Using cewel we can grab all the words from a page like this: cewl -m 4 -w wordlist.txt -d 0 -v http://127.0.0.1:5000/about

\-m 4: minimum word length is 4 characters\
&#x20;\-w wordlist: write output to file ‘wordlist’\
&#x20;\-d 0: follow links x times deep (0=stay on the same page)\
&#x20;\-v: verbose (show what you are doing)

Using a terminal window:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/7.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/8.png)

Let’s use burp intruder to calculate a sha-1 for every admin+word combination:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/9.png)

Payload position:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/10.png)

Paste the content of the word list in the payload options and add the payload processing rules as indicated in the following screenshot.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/11.png)

This will prefix the word 'admin' to each word from the list and calculate a sha1 of the concatenated string. for example sha1(adminBank)

Start the attack

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/12.png)

The result:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/13.png)

Now we can replace our cookie/sessionID with the value we found.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/14.png)

After going back to home page and proceeding to authenticaded section:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Auth-Bypass-2/15.png)

## Additional sources

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html" %}
