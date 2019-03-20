# KBID 104 - Content Type Headers


## Running the app

Becoming a super hero is a fairly straight forward process:

```text
$ sudo docker pull blabla1337/owasp-skf-lab:content-type 
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:content-type
```

{% hint style="success" %}

Now that the app is running let's go hacking! 

(.gitbook/assets/ING_Primary_Logo.png)

## Reconnaissance

Setting the right content headers is important for hardening your applications security, this reduces exposure to drive-by download attacks or sites serving user uploaded content that, by clever naming could be treated by MS Internet Explorer as executable or dynamic HTML files and thus can lead to security vulnerabilities.


An example of a content type header would be:

Content-Type: text/html; charset=UTF-8
or:
Content-Type: application/json;

Step 1:

To check if the user input is reflected lets see if the application accepts user input and reflects as part of the HTML. Lets input the following string, additionally you can also check how the application treats the dangerous HTML characters:

```text
xss
```

(.gitbook/assets/reco1.png)

Step2:

Lets check the response, for what looks like a JSON data however also notice the content-type to be set as text/html which looks suspicipus and can help us perform a Cross Site Scripting(XSS) attack. 

(.gitbook/assets/reco2.png)

(.gitbook/assets/reco3.png)

## Exploitation

Step 1:

With no content type headers restrictions imposed by the server, lets check if we can perform an XSS with the following string:

```text
<svg onload=alert(1)>
```
(.gitbook/assets/content1.png)

(.gitbook/assets/content2.png)

Step 2: Lets check how the application behaves to our malicious input, we notice the content-type is set to text/html and data looks like a JSON and we still succeed to perfrom a XSS attack:

(.gitbook/assets/content3.png)

(.gitbook/assets/content4.png)

(.gitbook/assets/content5.png)

Step 3:

With content type headers restrictions imposed by the server, lets check if we can perform an XSS with the following string:

```text
<svg onload=alert(1)>
```
(.gitbook/assets/content6.png)

We notice the content type in this situation is appropriately set to application/json and prevents the XSS attack. Additionally there should also be charset set accordingly.

(.gitbook/assets/content7.png)

(.gitbook/assets/content8.png)
