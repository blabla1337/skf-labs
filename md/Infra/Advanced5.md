# Advanced 5


####Building the machine with docker
```
docker build . -t advanced5
```
####Running the machine with docker
```
docker run  -h advanced5 -ti -p 80:80 -p 22:22 advanced5
```

## Reconnaissance
This lab is similar as the advanced3 and advanced4 lab. However, the privilege escalation is different and resembles a realistic scenario. If you've already performed the advanced3 or advanced4 lab, you can login into the machine with the credentials that you've discovered earlier and try to escalate your privileges

An nmap scan shows that ssh and http is open. Note: this is a docker instance that also shows the local windows ports. These are blurred in the screenshot as they are not relevant.
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/nmap.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

let's first check out the webpage:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/web.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We have a login page that we can fuzz with. 

## Exploitation
The first thing we try is SQL injection (ofcourse)... 
let's see what happens if we terminate the username and put the rest of the query in comment:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj1.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We get an error
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj1_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

That's a good thing !
So our query syntax is not correct. A few attemts show that commenting out with # instead of -- produce a correct syntax.

<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj2.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj2_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Lets try the basic sql injection
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj3.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The 'OR' seems to be filtered out
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj3_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Let's see if this is really the case:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj4.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

yes, the letter 'or' are filtered out:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj4_err.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Let's try to create an or with ||
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj5.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/inj5_ok.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Now we can try to login via SSH with the user john
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/ssh_login.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The web page may have hardcoded credentials to connect to a database. Let's check that out:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/credentials.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The database SkyTech has a user SkyTech with password Skytech.
Now we can login into mysql and explore the database:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/mysqllogin.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Let's figure out which tables there are in SkyTech
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/logintable.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We found some credentials, but they don't seem to work:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/loginfailed.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Let's checkout the admin database:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/accessdenied.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We're stuck here, but when we look at the file system, we notice a directory 'old' in the root of the file system.
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/dir_old.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The old directory contains an encrypted backup file and a backup script:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/backupscript.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

We can use the key from the backup script to decrypt the backup file:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/decrypt.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

By exploring the backup file, we can find the credentials of the Mysql root user:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/backupfile.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Now we can try if the system admins have defined the same password for the mysql root user and the linux root user. It seems we're lucky
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/advanced5/root.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

## Lessons learned
Vulnerabilities like sql injection may lead to information leakage and/or command execution. Proper input validation needs to be implemented by whitelisting allowed/expected characters. 
The mysql root account is not the same user as the root user from the operating system, in this case the administrators of the system gave both the same password, which is not recommended. Whenever possible, do not use local database users as applications need to store those credentials in order to connect to the backend database. Use windows integrated instead.
Left over files on the system, including backup files are vulnerabilities that are often encountered in real world scenario's. Keeping your systems clean is part of proper system management.
