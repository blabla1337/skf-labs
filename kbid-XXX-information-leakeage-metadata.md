# KBID XXX - Information Leakeage in Metadata (info-leakeage-metadata)
## Running the app
```text $ sudo python info-leakeage-metadata.py ``` ```text Visit the site: 
http://127.0.0.1:5000/ ``` {% hint style="success" %} Now that the app 
is running let's go hacking! {% endhint %} ![Docker Image and write-up 
thanks to TelecoLabs!](.gitbook/assets/telecolabs.png) shayu (shayubit) 
- https://www.telecolabs.com
## Reconnaissance
It is very common, and even recommended, for programmers to include detailed comments and metadata on their source code. 
However, comments and metadata included into the HTML code might reveal internal information that should not be available 
to potential attackers. Comments and metadata review should be done in order to determine if any information is being leaked.

When we start the application we can see that there is a login form.
![](.gitbook/assets/info-leakeage-meta-01.png)

## Exploitation
What we are going to do is explore and check the source code of the website in order to find some useful information that the programmer may have forgotten or hidden
in the source code and metadata tag and fields.
![](.gitbook/assets/info-leakeage-meta-02.png)

We found something promising inside two of the metadata tags!
Now, we try these words as the credentials in the login form:
![](.gitbook/assets/info-leakeage-meta-03.png)

And goal achieved!
![](.gitbook/assets/info-leakeage-meta-04.png)

## Additional sources
https://www.owasp.org/index.php/Review_webpage_comments_and_metadata_for_information_leakage_(OTG-INFO-005)
