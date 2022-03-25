#https://github.com/VinaykumarYennam/BsidesCharm-Vulnhub-VM-Walkthrough
#docker build . -t advanced1
#docker run  -h advanced1 -ti -p 80:80 -p 22:22 -p 21:21 -p 7000-7010:7000-7010 advanced1
# Note: Windows command line FTP does not support passive mode. use linux FTP to connect and type pass to switch to passive mode
# Alternatively use a windows client like filzilla to connect to the FTP server
FROM debian:buster-20210111-slim
RUN apt-get update
RUN apt-get install -y net-tools
RUN apt-get install -y sudo
RUN apt install -y vsftpd
RUN apt install inetutils-ping
RUN apt install ftp
RUN mkdir /var/ftp 
RUN mkdir /var/ftp/Public
COPY ./assets/users.txt.bk /var/ftp/Public/users.txt.bk
COPY ./assets/vsftpd.conf /etc/vsftpd.conf
RUN apt install -y ssh
COPY ./assets/sshd_config /etc/ssh/sshd_config
RUN echo 'root:SecPwdStr001' | chpasswd
RUN adduser --disabled-password -u 1001 --gecos "" abatchy & adduser --disabled-password -u 1002 --gecos "" john & adduser --disabled-password -u 1003 --gecos "" mai & adduser --disabled-password -u 1004 --gecos "" anne & adduser --disabled-password -u 1005 --gecos "" doomguy
RUN echo 'abatchy:AqRtZ123!' | chpasswd & "john:AqRtZ123!" | chpasswd & "mai:AqRtZ123!" | chpasswd & "doomguy:AqRtZ123!" | chpasswd
RUN echo 'anne:princess' | chpasswd 
RUN usermod -aG sudo anne
RUN apt-get -y install apache2
COPY ./assets/index.html /var/www/html/index.html
COPY ./assets/startup.sh /startup.sh
EXPOSE 21 22 7000-7010
ENTRYPOINT /startup.sh