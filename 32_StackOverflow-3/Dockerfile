FROM ubuntu:bionic
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

#Install dependencies
RUN apt-get update && apt-get install --fix-missing -y git \
bash \
python3-pip \
build-essential \
gcc \
gdb \
vim \
wget \
openssh-server \
net-tools

#Add a new user 
RUN useradd -ms /bin/bash stack
RUN echo "stack:stack" | chpasswd

#Setup the challenge
USER stack
WORKDIR /home/stack
COPY Stack-3/ /home/stack
USER root
RUN chmod u+s /home/stack/stack3

#Setup webssh
WORKDIR /
RUN git clone https://github.com/huashengdun/webssh
WORKDIR webssh
RUN python3 setup.py install

COPY start.sh /
RUN chmod +x /start.sh

CMD [ "/start.sh" ]
