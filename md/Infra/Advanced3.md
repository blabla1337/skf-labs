# Advanced 3


####Building the machine with docker
```
docker build . -t advanced3
```
####Running the machine with docker
```
docker run  -h advanced3 -ti -p 80:80 -p 22:22 advanced3
```

## Reconnaissance
An nmap scan shows that ssh and http is open. Note: this is a docker instance that also shows the local windows ports. These are blurred in the screenshot as they are not relevant.
<img  src="../../.gitbook/assets/infra/advanced3/nmap.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

let's first check out the webpage:
<img  src="../../.gitbook/assets/infra/advanced3/web.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We have a login page that we can fuzz with. 

## Exploitation
The first thing we try is SQL injection (ofcourse)... 
let's see what happens if we terminate the username and put the rest of the query in comment:
<img  src="../../.gitbook/assets/infra/advanced3/inj1.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We get an error
<img  src="../../.gitbook/assets/infra/advanced3/inj1_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

That's a good thing !
So our query syntax is not correct. A few attemts show that commenting out with # instead of -- produce a correct syntax.

<img  src="../../.gitbook/assets/infra/advanced3/inj2.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

<img  src="../../.gitbook/assets/infra/advanced3/inj2_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Lets try the basic sql injection
<img  src="../../.gitbook/assets/infra/advanced3/inj3.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The 'OR' seems to be filtered out
<img  src="../../.gitbook/assets/infra/advanced3/inj3_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Let's see if this is really the case:
<img  src="../../.gitbook/assets/infra/advanced3/inj4.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

yes, the letter 'or' are filtered out:
<img  src="../../.gitbook/assets/infra/advanced3/inj4_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Let's try to create an or with ||
<img  src="../../.gitbook/assets/infra/advanced3/inj5.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

<img  src="../../.gitbook/assets/infra/advanced3/inj5_ok.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Now we can try to login via SSH with the user john
<img  src="../../.gitbook/assets/infra/advanced3/Ssh_login.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The SSH session appears to terminate as soon as it connects, this could be due to a command specified in the .bashrc file. Let's remove this file by giving an ssh command line parameter:
<img  src="../../.gitbook/assets/infra/advanced3/ssh_login_rmbashrc.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Now we can try to login again:
<img  src="../../.gitbook/assets/infra/advanced3/ssh_john.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />


The login page may contain credentials to connect to a backend database. 
<img  src="../../.gitbook/assets/infra/advanced3/credentials.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />
We could also have guessed those ;-)

Now we can login into mysql:
<img  src="../../.gitbook/assets/infra/advanced3/mysqllogin.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

What do we have here:
<img  src="../../.gitbook/assets/infra/advanced3/tables.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We found clear text credentials
<img  src="../../.gitbook/assets/infra/advanced3/logins.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We can try to login with sara
<img  src="../../.gitbook/assets/infra/advanced3/ssh_sara.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Same batchrc issue here, we know what to do:
<img  src="../../.gitbook/assets/infra/advanced3/sara_batchrc.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

It appears that sara can execute the cat and ls command against all files in the /accounts directory:
<img  src="../../.gitbook/assets/infra/advanced3/sudo.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

<img  src="../../.gitbook/assets/infra/advanced3/root.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

<img  src="../../.gitbook/assets/infra/advanced3/su.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

## Lessons learned
Vulnerabilities like sql injection may lead to information leakage and/or command execution. Proper input validation needs to be implemented by whitelisting allowed/expected characters. Credentials should not be stored in clear text in databases. Password hashes should be stored instead.
Users should be given privileges according to the least privilege principle.
