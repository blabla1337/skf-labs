# Basic 4


####Building the machine with docker
```
docker build . -t basic4
```
####Running the machine with docker
```
docker run  -h basic4 -ti -p 22:22 basic4
```

## Reconnaissance
Imagine that a blackhat is hired to perform User Acceptance Tests on newly developed functionalities. He is given the username NPA_RunSvc_A with password AProm01* to login via ssh on the acceptance machine. He managed to obtain the server name of the production machine and will be payed a lot of money by a malicious third party if he can provide them access to that production machine. It's your job to test the security of this environment and recommend improvements if there are any.


## Exploitation
An nmap scan shows that only port 22 is open. We can try to force our login with a dictionary attack, but we'll need to do some guessing, make assumtions to find the right credentials in a timely fashion.
It is likely that the A at the end of the username stands 'acceptance' and the A in the beginning of the passwords also stands for acceptance. Maybe the production password is very similar. So lets try a combination of NPA_RunSvc_A and NPA_RunSvc_P with passwords starting with AProm and Pprom and varying numbers at the end. Lets also try another frequently used special character (!) at the end.

Creating such a password list can easily be accomplished with MSExcel.
The screenshot below shows the first few passwords in Excel and the formula that you can use to create them.
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic4/excel1.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

If we pull down our formula till number 99 with a '*' and till 99 with and '!' and this for 'Aprom' and 'PProm', we get 396 likely combinations:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic4/excel2.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

Lets paste the results in two text files:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic4/p.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic4/u.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />


Now we can try the credentials with 792 combinations using the following command:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic4/nmap1.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />

The screenshot below shows the password has been found:
<img  src="https://raw.githubusercontent.com/blabla1337/skf-labs/master/.gitbook/assets/infra/basic4/nmap2.png" style="box-shadow: 15px 15px 10px #999;  border: 1px solid #999" />


## Lessons learned
As simple as this exercise may be , easy guessable passwords is a vulnerability that is often encountered.
Although the passwords may be compliant to the password policy, having enough complexity, if they are deductable/guessable based on other known passwords, security can be easily breached. It is recommanded to differ passwords substantialy between the DTAP environments.
