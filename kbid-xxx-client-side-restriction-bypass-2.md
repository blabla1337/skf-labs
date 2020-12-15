# KBID XXX - Client Side Restriction Bypass, part 2

## Running the app

```text
$ sudo docker pull blabla1337/owasp-skf-lab:client-side-restriction-bypass-2
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:client-side-restriction-bypass-2
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Running the app Python3

First, make sure python3 and pip are installed on your host machine.
After installation, we go to the folder of the lab we want to practise 
"i.e /skf-labs/XSS/, /skf-labs/jwt-secret/ " and run the following commands:

```
$ pip3 install -r requirements.txt
```

```
$ python3 <labname>
```

{% hint style="success" %}
 Now that the app is running let's go hacking!
{% endhint %}


![Docker image and write-up thanks to Unixerius !](.gitbook/assets/Unixerius.png)


## Reconnaissance

{% hint style="info" %}
As we have done with previous labs, be sure to start Burp Suite so you can play along! Testing becomes so much easier if you use Burp's built-in Chrome web browser (tab **Proxy** > tab **Intercept** > button *Open Browser*).
{% endhint %}

Let us visit http://localhost:5000. It presents us with a familiar login screen. 

![](.gitbook/assets/csrb2-1.png)

For now, let's try user "admin" and password "admin". Which does let us inside!

![](.gitbook/assets/csrb2-2.png)

We're told that the "admin" user really likes the color blue and that they enjoy feasting on apple pie. That's great news! And since we're logged in as the user "admin", we can even update our favorite color! 

After submitting the form with a different color, the output has changed. 

![](.gitbook/assets/csrb2-3.png)

Let's take a look at Burp Suite's proxy history, to see what's happening in the background.

![](.gitbook/assets/csrb2-4.png)

Burp shows us that a POST request was made to http://localhost:5000/updatecolor. The form was submitted with one key:value pair, being "color=Green". 


## Exploitation

Looking into the HTTP requests in Burp, there appear to be no hidden form values that would allow us to change admin's favorite food. 

But let's try something! Maybe the web app is trying to hide some things in plain sight by simply not including them in the user interface. We can make a few guesses about what to try, no?

If you right-click the POST request in Burp's proxy history, you can select "*Send to Repeater*". This will light up the **Repeater** tab in orange, showing that something new appeared. Over there, we can edit the request before submitting it.

Let's change the called URL to http://localhost:5000/updatefood and let's change the form key to "food". Then if we click the "*Send*" button, maybe we'll get lucky!

![](.gitbook/assets/csrb2-5.png)

We did! And if you use the "*Refresh the page*" link (or the *Refresh* button of the browser) you'll see that the change is persistent. 

![](.gitbook/assets/csrb2-6.png)


## Additional sources

