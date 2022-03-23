chmod u+s /usr/bin/nmap
echo guest ALL=NOPASSWD:/usr/bin/nmap >> /etc/sudoers
service ssh start 
/bin/sh
