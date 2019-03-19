# Introduction

![OWASP security knowledge framework](.gitbook/assets/logo.svg)

Here we find all the labs and write-ups for the security knowledge framework!  
These labs are correlated to knowledge-base id's which are on their place  
again correlated to security controls such as from the ASVS or NIST, etc.

The labs are all downloadable from the following Github repository:

{% hint style="info" %}
[https://github.com/blabla1337/skf-labs](https://github.com/blabla1337/skf-labs)
{% endhint %}

The images can also be found on the skf docker hub. These skf-labs images are automatically pushed to the docker registry on each commit to the Github repository.

## Useful tools

First thing we need to do is to be able to investigate the requests that are being made by the labs/applications. We do this by setting up our intercepting proxy so we can gain more understanding of the application under test.

{% hint style="info" %}
Burp suite:  
[https://portswigger.net/burp/communitydownload](https://portswigger.net/burp/communitydownload)
{% endhint %}

{% hint style="info" %}
OWASP ZAP proxy:  
[https://www.owasp.org/index.php/OWASP\_Zed\_Attack\_Proxy\_Project](https://www.owasp.org/index.php/OWASP_Zed_Attack_Proxy_Project)
{% endhint %}

## How to add a Lab & write-up

When you want to contribute and add your own labs then please make sure you use the styling template in one of the lab challenges. We think its really important to have one look and feel and for able to merge your lab its required to use the SKF template. You can copy this from any of the labs we currently already have.

For adding the write-up for the lab we advice to create a copy of on existing write-up and work from there or use the template.md file as a base. You can store all your images in .gitbook/assets/ and also make sure you correlate your lab to one of the knowledge base item identifier in SKF. When you completed the lab and the write-up you only have to add it to the SUMMARY.md file and you are ready to create your Pull Request.

After the pull request you can find your nice styled write-up here:
https://owasp-skf.gitbook.io/asvs-write-ups/

