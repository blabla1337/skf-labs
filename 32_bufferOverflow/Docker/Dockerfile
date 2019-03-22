FROM i386/ubuntu:bionic
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN apt-get update && apt-get install -y git \
bash \
python-pip \
build-essential \
gcc \
gdb \
apache2

RUN pip install --upgrade pip setuptools
RUN pip install butterfly
RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/32_bufferOverflow
COPY ./ /var/www/html
RUN /etc/init.d/apache2 restart
CMD [ "bash", "butterfly.server.py --host='0.0.0.0' --unsecure" ]

