# Basic 2


####Building the machine with docker
```
docker build . -t basic2
```
####Running the machine with docker
```
docker run  -h basic2 -ti -p 22:22 basic2
```

## Reconnaissance

For this exercise you need to connect via SSH with user guest and password guest
The goal is to escalate privileges. It may be possible to find multiple ways to escalate privileges but in this case you should be looking at the storage of the passwords.

In the old days, passwords were stored in the /etc/passwd file.  Today, passwords hashes are stored in the /etc/shadow file (to which regular user have no read access) and the location in the passwd file were the hashes used to be present is now marked with x, indicating that they are stored in the shadow file.

Take a closer look at this mechanism to escalate your privileges.


## Exploitation
Let's login via ssh with guest/guest and look at the contents of the passwd file:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic2/passwdfile.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />


If we look at the /etc/passwd file we can see that we have write access !
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic2/writeaccess.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />


So we can edit the passwd file. If we remove the x in the second column of the /etc/passwd file, the password is set to blank !
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic2/editpasswd.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

After saving the file, we cannot login with ssh using the root account but we can switch the user to root !
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic2/swithctoroot.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

## Lessons learned
Sometimes system administrators change permissions to quickly solve a problem but forget to clean up/undo their actions.
It is recommended not to bypass safeguards and if an adhock situation emerges, honor the four eyes principle to avoid situations like this.