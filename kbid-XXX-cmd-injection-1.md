# KBID XXX - Command Injection 1 (CMD)

## Running the app

```text
$ sudo docker pull blabla1337/owasp-skf-lab:cmd
```

```text
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:cmd
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


![Docker image and write-up thanks to Contrahack.io !](.gitbook/assets/screen-shot-2019-03-04-at-21.33.32.png)


## Reconnaissance
The command injecion is an attack in which the goal is execution of
arbitrary commands on the host operating system via a vulnerable
application. Command injection attacks are possible when an application
passes unsafe user supplied data (forms, cookies, HTTP headers etc.) to
a system shell. In the first step, the attacker needs to inspect the
functioning of the web app in order to find possible injection points.
When we start the application we can see that there is an image and the option to resize the image.

![](.gitbook/assets/cmd01.png)

Now, we are going to select a value and press the button.

![](.gitbook/assets/cmd02.png)

If we inspect the request with an intercepting proxy \(we are using
Burp\) we can see that the application is performing a POST request to
/home. In the request we send the number (in pixels) to resize the image.
In the response, we can check that the image has been resized.

## Exploitation
For this lab we are going to try to write in the source code the output of a command executed in the system.

First, we check the source code:

![](.gitbook/assets/cmd05.0.png)

Now, we send a new HTTP request trying to write the output of the command
whoami (supposing that it will be executed in the target system) at the end of the index.html (main website view) code.

![](.gitbook/assets/cmd04.png)

Now we access the source code of the website

![](.gitbook/assets/cmd05.png)

to check that the output of the whoami command ("root") was written at the end of the source code.
As we can see, the output of the command whoami, is showing us the priviledge
of the target user in the target system and that the web app is actually
vulnerable to OS command injection.

## Mitigation
OS Command Injection can be prevented by following the methods described below:

Primary Defenses:

Option 1: Avoid calling OS Commands directly.

Option 2: Escaping values added to OS commands.

Option 3: Parameterization in conjunction with Input Validation

Additional Defenses:

Applications should run using the lowest privileges that are required to accomplish the necessary tasks.

If possible, create isolated accounts with limited privileges that are only used for a single task.



##### Avoid calling OS Commands directly.
In this case the primary defense is to avoid calling OS commands directly. Built-in library functions are a very good alternative to OS Commands, as they cannot be manipulated to perform tasks other than those it is intended to do.

Here, Lab functionality is to resize the image so we have python library which is PIL(Python Imaging Library).

The following code is vulnerable to OS Command injection:
PATH:/CMD/CMD.py
```
sizeImg = request.form['size']
os.system('convert static/img/bones.png -resize '+sizeImg+'% static/img/bones.png')
```

This is prevented by PIL library
PATH:/CMD/CMD.py
Import Library:
```
from PIL import Image
```

Code:
```
sizeImg = int(request.form['size'])
image = Image.open('static/img/bones.png')
new_image = image.resize((sizeImg, sizeImg))
new_image.save('static/img/resizeImg.png')
```

In kbid-XXX-cmd-injection-2 we have implemented another method i.e Escaping values added to OS commands.

## Additional sources
[https://www.owasp.org/index.php/Command\_Injection](https://www.owasp.org/index.php/Command_Injection)
