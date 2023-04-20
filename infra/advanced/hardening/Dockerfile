#https://github.com/vshaliii/Basic-Pentesting-1-Vulnhub-Walkthrough
#docker build . -t advanced2
#docker run  -h advanced2 -ti -p 80:80 -p 21:21 -p 7000-7010:7000-7010 advanced2
# Note: Windows command line FTP does not support passive mode. use linux FTP to connect and type pass to switch to passive mode
# Alternatively use a windows client like filzilla to connect to the FTP server
# https://ubuntu.com/tutorials/install-and-configure-wordpress#1-overview
FROM ubuntu:20.04
RUN apt update
RUN apt-get update
RUN apt-get install -y sudo net-tools ssh wget cron vim
RUN adduser --disabled-password -u 1004 --gecos "" anne
RUN echo 'anne:AqRtZ123!' | chpasswd
RUN echo "anne ALL=(ALL) NOPASSWD: /usr/bin/vim" >> /etc/sudoers
RUN adduser --disabled-password -u 1005 --gecos "" admin
RUN echo 'admin:SecPwdStr001' | chpasswd
RUN echo "SecPwdStr001 ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
COPY ./assets/persistance.sh /tmp


# -------- FTP--------
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y vsftpd ftp
RUN mkdir /var/ftp 
RUN mkdir /var/ftp/Public
COPY ./assets/vsftpd.conf /etc/vsftpd.conf
RUN echo 'anne:AqRtZ123!' >> /var/ftp/Public/test.sh
RUN echo "anne ALL=(ALL) NOPASSWD: /usr/bin/vim" >> /var/ftp/Public/test.sh
RUN chown ftp:ftp /var/ftp/Public/*


# -------- mysql --------
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install mysql-server
RUN echo [mysqld] >> /etc/mysql/my.cnf
RUN echo bind-address=0.0.0.0 >> /etc/mysql/my.cnf
RUN usermod -d /var/lib/mysql/ mysql


RUN apt-get -y install apache2 ghostscript libapache2-mod-php php php-bcmath php-curl php-imagick php-intl php-json php-mbstring php-mysql php-xml php-zip
COPY ./assets/wordpress.conf /etc/apache2/sites-available/wordpress.conf
COPY ./assets/wordpress_4.9.5+dfsg1-1_all.deb /var/tmp/wordpress_4.9.5+dfsg1-1_all.deb
RUN apt install -y /var/tmp/wordpress_4.9.5+dfsg1-1_all.deb
COPY ./assets/wordpress.sql /var/tmp/wordpress.sql
COPY ./assets/tracker.php /var/www/html/tracker.php
COPY ./assets/startup.sh /startup.sh
RUN chmod +x /startup.sh

USER admin
RUN crontab -l | { cat; echo "*/5 * * * * /tmp/persistance.sh"; } | crontab - 
USER root

EXPOSE 21 22 80 443 3306 7000-7010
ENTRYPOINT /startup.sh 