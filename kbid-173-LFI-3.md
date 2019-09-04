# KBID xxx - LFI-3


## Running the app


```text
$ sudo docker pull blabla1337/owasp-skf-lab:LFI-3
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:LFI-3
```

{% hint style="success" %}

Now that the app is running let's go hacking! 

![Docker image and write-up thanks to ING!](.gitbook/assets/ing_primary_logo.png)

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

We could try to modify the "intro" item and attempt to access the world-readable /etc/passwd file by directory traversal. 
This will not work since the webserver does not accept the '../' sequence at all.

We might success if we URL encode our payload(../../../../../../../etc/passwd) like this:

```Text
%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
```
It seems not to work...

Let's try to double URL encode our payload like this:
```Text
%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd
```
Or like this:
```Text
%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%25%32%65%25%32%65%25%32%66%65%74%63%25%32%66%70%61%73%73%77%64
```

![](.gitbook/assets/LFI-3_devtools.png)
![](.gitbook/assets/LFI-3_result.png)

{% hint style="success" %} Success! As we observed, we can access the /etc/passwd file through LFI.

## Additional sources

https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion 
