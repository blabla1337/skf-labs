# --------- Image +  build & Run----------
#docker build . -t basic5
#docker run  -h basic5 -ti -p 22:22 -p 3306:3306 basic5
FROM ubuntu:20.04
RUN apt update
RUN apt-get update

# --------- mysql----------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install mysql-server
RUN echo [mysqld] >> /etc/mysql/my.cnf
RUN echo bind-address=0.0.0.0 >> /etc/mysql/my.cnf
RUN usermod -d /var/lib/mysql/ mysql
COPY ./assets/Admin.sql /var/tmp/Admin.sql
#The queries to allow root to login remotely ar run after service startup in /startup.sh

# --------- general stuff ----------
#RUN apt-get install -y net-tools
#RUN apt-get install -y sudo
RUN apt install -y inetutils-ping
RUN apt install -y nano
RUN apt install -y cron

# --------- FTP ----------
# RUN apt install -y vsftpd
# RUN mkdir /var/ftp 
# RUN mkdir /var/ftp/Public
# COPY ./assets/users.txt.bk /var/ftp/Public/users.txt.bk
# COPY ./assets/vsftpd.conf /etc/vsftpd.conf
# Note: Windows command line FTP does not support passive mode. use linux FTP to connect and type pass to switch to passive mode
# Alternatively use a windows client like filzilla to connect to the FTP server

# --------- ssh ----------
RUN apt install -y ssh
COPY ./assets/sshd_config /etc/ssh/sshd_config

# --------- users ----------
RUN echo 'root:String001' | chpasswd
RUN adduser --disabled-password -u 1001 --gecos "" guest
RUN echo 'guest:guest' | chpasswd 

# --------- backup ----------
RUN mkdir /var/backup
RUN echo "mysqldump --password=root --user=root Admin > /var/backups/Admin.sql 2> /dev/null" > /var/backup/backup.sh
RUN chmod 777 /var/backup/backup.sh

# --------- start ----------
COPY ./assets/startup.sh /startup.sh
EXPOSE  22 3306 
ENTRYPOINT /startup.sh