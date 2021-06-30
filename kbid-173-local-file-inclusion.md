# KBID 173 - Local File Inclusion


## Running the app


```text
$ sudo docker pull blabla1337/owasp-skf-lab:lfi
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:lfi
```

{% hint style="success" %}

Now that the app is running let's go hacking!

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


![Docker image and write-up thanks to Contrahack.io !](.gitbook/assets/screen-shot-2019-03-04-at-21.33.32.png)

## Reconnaissance

Local File Inclusion (also known as LFI) is the process of including files, that are already locally present on the server, through the exploiting of vulnerable inclusion procedures implemented in the application. This vulnerability occurs, for example, when a page receives, as input, the path to the file that has to be included and this input is not properly sanitized, allowing directory traversal characters (such as dot-dot-slash) to be injected. Although most examples point to vulnerable PHP scripts, we should keep in mind that it is also common in other technologies such as JSP, ASP and others.

Warning: To successfully test for this flaw, the tester needs to have knowledge of the system being tested and the location of the files being requested. There is no point requesting /etc/passwd from an IIS web server.

Some Examples:

```text
http://example.com/getUserProfile.jsp?item=../../../../etc/passwd

Cookie: USER=1826cc8f:PSTYLE=../../../../etc/passwd
```

## Exploitation

The File Inclusion vulnerability allows an attacker to include a file, usually exploiting a "dynamic file inclusion" mechanisms implemented in the target application. The vulnerability occurs due to the use of user-supplied input without proper validation.

This can lead to something as outputting the contents of the file, but depending on the severity, it can also lead to:

Code execution on the web server

Code execution on the client-side such as JavaScript

which can lead to other attacks such as:

Cross-site scripting (XSS)

Denial of Service (DoS)

Sensitive Information Disclosure

Let us see how can we exploit the file inclusion vulnerability in a real world scenario, the application here allows us to view details on Intro, Chapter1, Chapter2 and so on.

![](.gitbook/assets/lfi1.png)

![](.gitbook/assets/lfi2.png)

To exploit let us try to modify the "Intro item" and attempt to access the world-readable /etc/passwd file by directory traversal.

![](.gitbook/assets/lfi3.png)

![](.gitbook/assets/lfi4.png)

{% hint style="success" %} Success! As we observed, we can access the /etc/passwd file through LFI.

## Mitigation

For mitigating the most effective approach would be to avoid user controlled inputs additionally we can use:
1) Indexing
2) Whitelisting

In this case, we are presented a fix by the using Indexing approach.

In the following vulnerable code, as there isn't any form of validation an attacker can manipulate the inputs to fetch any files present on the server:

![](.gitbook/assets/LFI1old.png)

For the fix, we also would update the Front-End code to assign indexes instead of direct filename:

![](.gitbook/assets/LFIhtml.png)

For indexing we created a lookup table using the if-else statement or we could also use dictionary:

![](.gitbook/assets/LFI1new.png)

In the kbid-173-LFI-2, we have implemented Whitelisting if you wish to check.

Can you think of other cool solutions to fix the local file inclusion vulnerability?

## Additional sources

https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion
