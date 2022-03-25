# --------- Image +  build & Run----------
#docker build . -t advanced5
#docker run  -h 8dvanced5 -ti -p 80:80 -p 22:22 advanced5
#Skytower from sqli to root, a realistic way

FROM debian:buster-20210111-slim
RUN apt-get update

# --------- mysql----------
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -q -y install default-mysql-server
RUN echo [mysqld] >> /etc/mysql/my.cnf
RUN echo bind-address=0.0.0.0 >> /etc/mysql/my.cnf
RUN usermod -d /var/lib/mysql/ mysql
COPY ./assets/SkyTech.sql /var/tmp/SkyTech.sql
COPY ./assets/Admin.sql /var/tmp/Admin.sql
RUN mkdir /old
COPY ./assets/backup.enc /old/backup.enc
COPY ./assets/backup.sh /old/backup.sh


# --------- general stuff ----------exit
#RUN apt-get install -y sudo
# RUN apt install -y inetutils-ping
# RUN apt install -y ftp

# --------- ssh ----------
RUN apt install -y ssh
COPY ./assets/sshd_config /etc/ssh/sshd_config

# --------- users ----------
RUN echo 'root:admin12345678' | chpasswd
RUN adduser --disabled-password -u 1001 --gecos "" john
RUN echo 'john:hereisjohn' | chpasswd

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