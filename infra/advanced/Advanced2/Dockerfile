#https://github.com/vshaliii/Basic-Pentesting-1-Vulnhub-Walkthrough
#docker build . -t advanced2
#docker run  -h advanced2 -ti -p 80:80 -p 21:21 -p 7000-7010:7000-7010 advanced2
# Note: Windows command line FTP does not support passive mode. use linux FTP to connect and type pass to switch to passive mode
# Alternatively use a windows client like filzilla to connect to the FTP server
# https://ubuntu.com/tutorials/install-and-configure-wordpress#1-overview
FROM ubuntu:20.04
RUN apt update
RUN apt-get update
RUN apt-get install -y net-tools
RUN apt-get install -y sudo
RUN apt-get install -y wget
RUN apt-get install -y cron

# -------- FTP--------
COPY ./assets/proftpd-basic_1.3.5e-1build1_amd64.deb /var/tmp/proftpd-basic_1.3.5e-1build1_amd64.deb
RUN apt install -y /var/tmp/proftpd-basic_1.3.5e-1build1_amd64.deb
COPY ./assets/proftpd/proftpd.conf /etc/proftpd/proftpd.conf
COPY ./assets/proftpd/proftpd /usr/sbin/proftpd
COPY ./assets/proftpd/proftpd.delay /usr/local/var/proftpd.delay
RUN chmod 777 /usr/sbin/proftpd

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
COPY ./assets/startup.sh /startup.sh
RUN chmod +x /startup.sh
EXPOSE 21 80 7000-7010
ENTRYPOINT /startup.sh 