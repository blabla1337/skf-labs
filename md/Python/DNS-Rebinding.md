# DNS Rebinding

## Running the app on Docker

```
$ sudo docker pull blabla1337/owasp-skf-lab:<TBD>
```

```
$ sudo docker run -ti -p 127.0.0.1:5000:5000 blabla1337/<TBD>>
```

{% hint style="success" %}
Now that the app is running let's go hacking!
{% endhint %}

## Reconnaissance

DNS Rebinding lets you send commands to systems behind a victim’s firewall, as long as they’ve somehow come to a domain you own asking for a resource, and you’re able to run JavaScript in their browser.

The attacker initiates repeated DNS queries to a domain under their control. The first query would return a valid response that passes security checks, while subsequent queries return a malicious response that targets the internal network.

It requires a bit about the victim in order to accomplish the access,
for example, know which browser the victim used, know the IP subnet of the victim’s network, etc.

It is a trial and error to check which internally running services are accessible in which network subnet.

## Exploitation

Let's check it a little bit deeper the application responses.
There is a running service locally on port 80. We need a DNS service which resolves the same local IP address as localhost.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/DNS-Rebinding/1.png)

It is seen in the below code snippet that the DNS resolution is performed and only DNS names that resolves 127.0.0.1 are allowed to access that resource. Immediately we think of 'localhost' which is by default resolves as 127.0.0.1, but it is restricted. 

```
if((str(request.args.get('hostname')).lower() == "localhost".lower() or str(request.args.get('hostname') == "127.0.0.1") and not re.search('[A-Za-z]+', str(request.args.get('hostname'))))):
        return render_template("index.html", read = "'localhost' and '127.0.0.1' are filtered but... (un)luckily the DNS resolution is performed afterwards this filter.")
    else:
        try:
            if (socket.gethostbyname(request.args.get('hostname')) == "127.0.0.1"): # just to prevent SSRF against other websites
                return render_template("index.html", read = requests.get("http://" + request.args.get('hostname')).text)
            else:
                return render_template("index.html", read = "Only loopback requests are allowed here.")
        except:
    	        return render_template("index.html", read = "The service to access is listening on localhost (port 80). For DNS rebinding attacks you are expected to control the DNS resolution. </br>For such purpose, you have to setup an authoritative DNS for one of your domains... or use one already <a href=\"https://github.com/brannondorsey/whonow\">available</a>.")

```

The localhost is not allowed, therefore we should find a way such that provided DNS name will be resolved as 127.0.0.1.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/DNS-Rebinding/2.png)


As a solution, we can setup a rogue DNS server that returns 127.0.0.1 for specific DNS names.
We can use [whonow](github.com/brannondorsey/whonow) tool to run a rogue DNS server. This tool should be installed on a externally reachable server or use [Singularity of Origin Tool](http://rebind.it/) to test applications that are reachable from the Internet.

```
Installing 'whonow' tool:

sudo npm update
sudo npm install --cli -g whonow@latest
```

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/DNS-Rebinding/3.png)


After running the whonow DNS server, we can test if we resolve expected local IP and it resolves the DNS name as expected (127.0.0.1).
The DNS naming convention for whonow names is given as below. So we can change the way we want to test the environment.

```
A.<ip-address>.<rule>[.<ip-address>.<rule>[.<ip-address>.<rule>]][.uuid/random-string].rebind.network
```


![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/DNS-Rebinding/4.png)


Having the working rogue DNS server, we can try to resolve this DNS on our lab. The response shows that we are able to access to the service running on 127.0.0.1:80 using a rogue DNS server with a custom DNS name.

![](https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/python/DNS-Rebinding/5.png)

## Additional sources

{% embed url="https://portswigger.net/web-security/sql-injection/lab-login-bypass" %}
