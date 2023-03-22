# Credentials Guessing 2

## Running the app on Docker

```text
$ sudo docker pull blabla1337/owasp-skf-lab:credentials-guessing-2
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:credentials-guessing-2
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

It is very common to use very guessable and weak usernames and passwords because they are easier to use and remember.
However, this ease for the users becomes a great advantage for potential attackers who are trying to crack the user's credentials.
It is pretty easy for them to guess or brute force many different credentials until they get to the right ones.

When we start the application we can see that there is a login form.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/1.png)

If we try with some wrong and random credentials such as: [ admin:admin ], we don`t get access to the inside of the website and an error message is displayed:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/2.png)

## Exploitation

Provided that once the username is incorrect it will appear an error message and supossing that once it is correct, this message will not appear,
we will use Burp in order to brute force different usernames and discover the right one by analysing the length of the HTTP responses for each trial.
We use the "Intruder" functionality and we will load a prefixed dictionary with multiple usernames that will be tried against the website one by one.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/3.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/4.png)

If we check the lenght of the different HTTP responses for each of the password that Burp tried, we find that there's one with a different length than
the rest of the possibilities:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/5.png)

We found something promising! This must be the desired username.

We can check now sending the HTTP request using this word as the username:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/6.png)

No error messages are now displayed (which means that this username must be correct):

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/7.png)

Now, if we follow the same methodology for the password or we simply try the username as the password in the login form, we will get access to the inside
of the website:

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/8.png)

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/Credentials-Guessing-2/9.png)

And goal achieved!

## Additional sources

https://www.owasp.org/index.php/Testing_for_User_Enumeration_and_Guessable_User_Account_(OWASP-AT-002)
