# --------- Image +  build & Run----------
#docker build . -t basic1
#docker run  -h Basic1 -ti -p 80:80 -p 22:22 -p 21:21 -p 3306:3306 -p 7000-7010:7000-7010 basic1
FROM ubuntu:20.04
RUN apt update
RUN apt-get update

# --------- mysql----------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install mysql-server
RUN echo [mysqld] >> /etc/mysql/my.cnf
RUN echo bind-address=0.0.0.0 >> /etc/mysql/my.cnf
RUN usermod -d /var/lib/mysql/ mysql
#The queries to allow root to login remotely ar run after service startup in /startup.sh

# --------- general stuff ----------
#RUN apt-get install -y net-tools
RUN apt-get install -y sudo
RUN apt install -y inetutils-ping
RUN apt install -y ftp

# --------- FTP ----------
RUN apt install -y vsftpd
RUN mkdir /var/ftp 
RUN mkdir /var/ftp/Public
COPY ./assets/users.txt.bk /var/ftp/Public/users.txt.bk
COPY ./assets/vsftpd.conf /etc/vsftpd.conf
# Note: Windows command line FTP does not support passive mode. use linux FTP to connect and type pass to switch to passive mode
# Alternatively use a windows client like filzilla to connect to the FTP server

# --------- ssh ----------
RUN apt install -y ssh
COPY ./assets/sshd_config /etc/ssh/sshd_config

# --------- users ----------
RUN echo 'root:String001' | chpasswd
RUN adduser --disabled-password -u 1001 --gecos "" abatchy & adduser --disabled-password -u 1002 --gecos "" john & adduser --disabled-password -u 1003 --gecos "" mai & adduser --disabled-password -u 1004 --gecos "" anne & adduser --disabled-password -u 1005 --gecos "" doomguy
RUN echo 'abatchy:AqRtZ123!' | chpasswd & "john:AqRtZ123!" | chpasswd & "mai:AqRtZ123!" | chpasswd & "doomguy:AqRtZ123!" | chpasswd
RUN echo 'anne:princess' | chpasswd 
RUN usermod -aG sudo anne

# --------- apache ----------
RUN apt-get -y install apache2
COPY ./assets/index.html /var/www/html/index.html

# --------- start ----------
COPY ./assets/startup.sh /startup.sh
# EXPOSE 21 22 3306 7000-7010 
ENTRYPOINT /startup.sh