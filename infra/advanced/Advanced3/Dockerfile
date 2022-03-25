# --------- Image +  build & Run----------
#docker build . -t advanced3
#docker run  -h Advanced3 -ti -p 80:80 -p 22:22 advanced3
#note: removing the .bashrc file is a bit harder then in the write up 
#      Some extra quotes are required: ssh -t john@localhost "rm '.bashrc'"
#      On this machine port 22 is not filtered

FROM debian:buster-20210111-slim

# --------- mysql----------
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install default-mysql-server
RUN echo [mysqld] >> /etc/mysql/my.cnf
RUN echo bind-address=0.0.0.0 >> /etc/mysql/my.cnf
RUN usermod -d /var/lib/mysql/ mysql
COPY ./assets/SkyTech.sql /var/tmp/SkyTech.sql

# --------- general stuff ----------exit
RUN apt-get install -y sudo
# RUN apt install -y inetutils-ping
# RUN apt install -y ftp

# --------- ssh ----------
RUN apt install -y ssh
COPY ./assets/sshd_config /etc/ssh/sshd_config

# --------- users ----------
RUN echo 'root:theskytower' | chpasswd
COPY ./assets/flag.txt /root/flag.txt
RUN adduser --disabled-password -u 1001 --gecos "" john & adduser --disabled-password -u 1002 --gecos "" sara
COPY ./assets/.bashrc /home/john/.bashrc
COPY ./assets/.bashrc /home/sara/.bashrc
RUN echo 'sara:ihatethisjob' | chpasswd 
RUN echo 'john:hereisjohn' | chpasswd  
RUN mkdir accounts
RUN echo "sara ALL=(ALL) NOPASSWD: /bin/cat /accounts/* , /bin/ls /accounts/* " > /etc/sudoers


# --------- apache ----------
RUN apt-get -y install apache2
RUN apt install -y php libapache2-mod-php php-mysql
COPY ./assets/www/ /var/www/
COPY ./assets/etc/apache2/sites-available /etc/apache2/sites-available
COPY ./assets/etc/apache2/sites-enabled /etc/apache2/sites-enabled

# --------- start ----------
COPY ./assets/startup.sh /startup.sh
EXPOSE 22 80
ENTRYPOINT /startup.sh