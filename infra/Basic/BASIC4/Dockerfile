# --------- Image +  build & Run----------
#docker build . -t basic4
#docker run  -h basic4 -ti -p 22:22 basic4
FROM ubuntu:20.04
RUN apt update


# --------- Optional general stuff ----------
# RUN apt-get install -y net-tools
#RUN apt-get install -y sudo
#RUN apt install -y nmap
# RUN apt install -y inetutils-ping
# RUN apt install -y ftp


# --------- ssh ----------
RUN apt install -y ssh
#COPY ./assets/sshd_config /etc/ssh/sshd_config

# --------- users ----------
RUN echo 'root:String001' | chpasswd
RUN adduser --disabled-password --force-badname -u 1001 --gecos "" NPA_Run_SvcP 
RUN echo 'NPA_Run_SvcP:PProm02*' | chpasswd


# --------- start ----------
COPY ./assets/startup.sh /startup.sh
EXPOSE 22 
ENTRYPOINT /startup.sh