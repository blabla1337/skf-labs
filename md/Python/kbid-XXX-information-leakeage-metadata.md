# KBID XXX - Information Leakeage in Metadata

## Running the app

```
$ sudo docker pull blabla1337/owasp-skf-lab:info-leakeage-metadata
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:info-leakeage-metadata
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

![Docker image and write-up thanks to Contrahack.io !](../../.gitbook/assets/screen-shot-2019-03-04-at-21.33.32.png)

## Reconnaissance

It is very common, and even recommended, for programmers to include detailed comments and metadata on their source code. However, comments and metadata included into the HTML code might reveal internal information that should not be available to potential attackers. Comments and metadata review should be done in order to determine if any information is being leaked.

When we start the application we can see that there is a login form.

![](../../.gitbook/assets/info-leakeage-meta-01.png)

## Exploitation

What we are going to do is explore and check the source code of the website in order to find some useful information that the programmer may have forgotten or hidden in the source code and metadata tag and fields.

![](../../.gitbook/assets/info-leakeage-meta-02.png)

We found something promising inside two of the metadata tags! Now, we try these words as the credentials in the login form:

![](../../.gitbook/assets/info-leakeage-meta-03.png)

And goal achieved!

![](../../.gitbook/assets/info-leakeage-meta-04.png)

## Additional sources

[https://www.owasp.org/index.php/Review_webpage_comments_and_metadata_for_information_leakage\_(OTG-INFO-005](https://www.owasp.org/index.php/Review_webpage_comments_and_metadata_for_information_leakage_(OTG-INFO-005))
