# KBID 44 - Authorisation missing

## Running the app

```text
$ sudo docker pull blabla1337/owasp-skf-lab:auth-missing
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:auth-missing
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

![Docker Image and write-up thanks to TelecoLabs!](.gitbook/assets/telecolabs.png)

Alberto Rafael Rodríguez Iglesias - www.telecolabs.com

## Reconnaissance

The session prediction attack focuses on predicting session ID values that permit an attacker to bypass the authentication schema of an application. By analyzing and understanding the session ID generation process, an attacker can predict a valid session ID value and get access to the application.

In the first step, the attacker needs to collect some valid session ID values that are used to identify authenticated users. Then, he must understand the structure of session ID, the information that is used to create it, and the encryption or hash algorithm used by application to protect it. Some bad implementations use sessions IDs composed by username or other predictable information, like timestamp or client IP address. In the worst case, this information is used in clear text or coded using some weak algorithm like base64 encoding.

In addition, the attacker can implement a brute force technique to generate and test different values of session ID until he successfully gets access to the application.

![](.gitbook/assets/inicio.png)

When start the application we can see that we have a "create new user" functionality and we will be redirected to out private user space. First let's try to create a new user to see how the application behaves.

![](.gitbook/assets/new_user_req.png)

If we inspect the request with an intercepting proxy \(we are using Burp\) we can see that the application is performing a POST request to /signup:

![](.gitbook/assets/successful_new_user.png)

From there we can access our private user's space using a GET request, that we analyze below:

![](.gitbook/assets/private_space_new_user.png)

## Exploitation

It seems that the only parameter which takes care of which private space we are shown is the userID. Now we will try different possibilities for the userID by changing the number to similar ones:

Lets try with user02.

![](.gitbook/assets/private_space_admin.png)

As you can see we got access to another user's account whose ID was 02. This proves the weak mechanism of sessions management implemented here. Thanks to it, we can get all the user's private information. In this case this allow us to get admin credentials for the website.

We could keep trying to discover other resources for useful information. Let's try to explore other accounts like user01.

## Additional sources

[https://www.owasp.org/index.php/Session\_Prediction](https://www.owasp.org/index.php/Session_Prediction)

