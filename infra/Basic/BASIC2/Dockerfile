# --------- Image +  build & Run----------
#docker build . -t basic2
#docker run  -h basic2 -ti -p 22:22 basic2
FROM ubuntu:20.04
RUN apt update


# --------- Optional general stuff ----------
# RUN apt-get install -y net-tools
# RUN apt-get install -y sudo
# RUN apt install -y inetutils-ping
# RUN apt install -y ftp


# --------- ssh ----------
RUN apt install -y ssh
COPY ./assets/sshd_config /etc/ssh/sshd_config

# --------- users ----------
RUN echo 'root:String001' | chpasswd
RUN adduser --disabled-password -u 1001 --gecos "" guest 
RUN echo 'guest:guest' | chpasswd
RUN chmod 777 /etc/passwd


# --------- start ----------
COPY ./assets/startup.sh /startup.sh
EXPOSE 22 
ENTRYPOINT /startup.sh