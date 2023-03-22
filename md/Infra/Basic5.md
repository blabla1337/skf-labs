# Basic 5


####Building the machine with docker
```
docker build . -t basic5
```
####Running the machine with docker
```
docker run  -h basic5 -ti -p 22:22 basic5
```

## Reconnaissance
A system administrators has granted you access to a database server. You can login to this system using guest credentials (guest/guest). Your goal is to escalate privileges on this machine.

<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/ssh_login.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

## Exploitation
A database server needs backups of its database, which is normally an automated job with higher privileges. Let's investigate this to see if we can exploit the higher privileges that are in use.
We can check which software is installed to see if a specific package like automysqlbackup is in use. 
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/dpkg.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The result doesn't show anything familiar.
On windows machine we would look into the scheduled tasks. Here, on a linux machine we'll look into the cron jobs to see whether the admins create a backup scheduling them selves.

As quest user we can't see a schedueled job for the backups.
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/cron.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Maybe we can find something on the file system:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/backup.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />
If we look closely at the backup file, we see that it is only one minute old.
A minute later we see it has been replaced. Aparently something is creating the backups.
the backup script has write access, so we can edit it.
We see the credentials of the root user in this script !
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/su.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />
Too bad, the root user of the mysql user has a different password then the linux root user.

Ok, let's try to edit the the script then. We add two commands to add a user non-interactively. Please note running commands from the command line differs from running commands in a cron job (we suspect this is what the script triggers), therefore we explicitly specify the path to the executables.
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/add_user.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Within a minute we should have created a new user if the script is indeed running under a high privileged user. Yes ! we can login and we're root !
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic5/new_user_login.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />



## Lessons learned
Improper file system permissions often lead to privilege escalation possibilities. In this case the system admin misconfigured the access rights on the backup script. 
Also on Windows systems misconfigured NTFS permissions may lead to privilege escalation possibilities. On windows systems we recommend to investigate any software that is installed in other directories then "C:\program files (x86)" and "C:\program files" as only software installed in those folders have proper access rights by default.
