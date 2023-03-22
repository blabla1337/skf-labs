# Advanced x


####Building the machine with docker
```
docker build . -t advanced1
```
####Running the machine with docker
```
docker run  -h advanced1 -ti -p 80:80 -p 22:22 -p 21:21 -p 7000-7010:7000-7010 advanced1
```

## Reconnaissance
This lab is similar to the 'vancouver' virtual machine that you can find on vulnhub
you can follow the walkthrough that you can find here https://github.com/VinaykumarYennam/BsidesCharm-Vulnhub-VM-Walkthrough
Note: Windows command line FTP does not support passive mode. Alternatively, you can use a windows client like FileZilla to connect to the FTP server.

In the screenshot below, we're scanning the docker image on localhost on a windows machine. The ports that are exposed by the docker image are marked in yellow:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/nmap.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We spotted a website but there is nothing but a login page that says it works...
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/web.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We tried nikto but it also didn't yield anything
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/nikto.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

So lets try to make an anonymous connection to the FTP server:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/filezilla1.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We can find a leftover file users.txt.bk here:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/filezilla2.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />


The following users were found:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/users.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

## Exploitation
Lets try these account with a blank password on ssh. We are lucky, one of the users allows to login with regular password instead of a public key.
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/ssh.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

now we can try to perform a dictionary attack using hydra:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/hydra.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

SSH login with anne/princess
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/sshlogin.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

lets see if ann can sudo some commands
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced1/sudo.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

## Lessons learned
Always keep your servers clean. Left behind files are often an entry point that helps malicious users to exploit vulnerabilities.
Applications/services that can be attacked with a dictionary attack due to missing lockout mechanisms are prone to be compromised at some point in time.
Users should only be assigned the least amount of privileges that he/she needs to perform the job.
