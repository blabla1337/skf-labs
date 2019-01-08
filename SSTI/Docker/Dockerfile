FROM alpine:3.7
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>
RUN apk update --no-cache && apk add git \
python2-dev \
py2-pip \ 
git \
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/LFI
RUN pip install -r requirements.txt
CMD [ "python2", "./SSTI.py" ]