FROM i386/ubuntu:bionic
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN apt-get update && apt-get install -y git \
bash \
python-pip \
build-essential \
gcc \
gdb \
apache2

RUN dpkg --add-architecture i386
RUN pip install --upgrade pip setuptools
RUN pip install butterfly
RUN git clone https://github.com/blabla1337/skf-labs.git

#WORKDIR /skf-labs

COPY entrypoint.sh /
COPY start.sh /


RUN ["chmod", "+x", "/entrypoint.sh"]
RUN ["chmod", "+x", "/start.sh"]
ENTRYPOINT [ "/entrypoint.sh" ]

#docker build . -t test
#docker run  -ti -p 127.0.0.1:80:80 -p 127.0.0.1:57575:57575 test