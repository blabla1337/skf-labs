FROM i386/ubuntu:bionic
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN apt-get update && apt-get install -y git \
bash \
python-pip \
build-essential \
libssl-dev \
gcc \
gdb \
vim \
wget \
apache2

RUN dpkg --add-architecture i386
RUN pip install --upgrade pip setuptools
RUN pip install butterfly

#start Apache
CMD ["/etc/init.d/apache2 start"]

#Add stack user
RUN useradd -ms /bin/bash stack
#Add stack password
RUN echo "stack:stack" | chpasswd
USER stack
WORKDIR /home/stack
RUN git clone https://github.com/blabla1337/skf-labs.git
USER root
RUN cp -r /home/stack/skf-labs/32_bufferOverflow/static /var/www/html
RUN cp /home/stack/skf-labs/32_bufferOverflow/index.html /var/www/html
USER stack
RUN cp -r /home/stack/skf-labs/32_bufferOverflow/Stack-0 /home/stack
RUN rm -r /home/stack/skf-labs
USER root
RUN chmod u+s /home/stack/Stack-0/stack0
COPY motd /usr/local/lib/python2.7/dist-packages/butterfly/templates/motd
COPY entrypoint.sh /
COPY start.sh /

ENTRYPOINT [ "/entrypoint.sh" ]

#docker build . -t stack
#docker run  -ti -p 127.0.0.1:80:80 -p 127.0.0.1:57575:57575 stack
#Go to http://127.0.0.1 and login with user:stack pass:stack