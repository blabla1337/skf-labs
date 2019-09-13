# KBID XXX - Credentials Guessing 3 (credentials-guessing-3)
## Running the app
```text $ sudo python credentials-guessing-3.py ``` ```text Visit the site: 
http://127.0.0.1:5000/ ``` {% hint style="success" %} Now that the app 
is running let's go hacking! {% endhint %} ![Docker Image and write-up 
thanks to TelecoLabs!](.gitbook/assets/telecolabs.png) shayu (shayubit) 
- https://www.telecolabs.com

## Reconnaissance

It is very common to use very guessable and weak usernames and passwords because they are easier to use and remember. 
However, this ease for the users becomes a great advantage for potential attackers who are trying to crack the user's credentials. 
It is pretty easy for them to guess or brute force many different credentials until they get to the right ones.

When we start the application we can see that there is a login form.

![](.gitbook/assets/cred-guessing-30.png)

If we try with some wrong and random credentials such as: [ asdf:asdf ], we don`t get access to the inside of the website and an error message is displayed:

![](.gitbook/assets/cred-guessing-31.png)

It says that the username is incorrect.

## Exploitation
Provided that once the username is incorrect it will appear an error message and supossing that once it is correct, this message will not appear (or at least it will have a different length), 
we will use Burp in order to brute force different usernames and discover the right one by analysing the length of the HTTP responses for each trial.
We use the "Intruder" functionality and we will load a prefixed dictionary with multiple usernames that will be tried against the website one by one.

![](.gitbook/assets/cred-guessing-32.png)

If we check the lenght of the different HTTP responses for each of the password that Burp tried, we find that there's one with a different length than
the rest of the possibilities:

![](.gitbook/assets/cred-guessing-33.png)


We have found something promising! This must be the desired username.

We can check now sending the HTTP request using this word as the username:

![](.gitbook/assets/cred-guessing-34.png)

No error messages related to a wront username is displayed now (which means that this username must be correct), but it now says that the password is incorrect:

![](.gitbook/assets/cred-guessing-35.png)

Now, if we follow the same methodology for the password, we will find the right password and get access to the inside of the website:

![](.gitbook/assets/cred-guessing-36.png)

And goal achieved!

## Additional sources
https://www.owasp.org/index.php/Testing_for_User_Enumeration_and_Guessable_User_Account_(OWASP-AT-002)
