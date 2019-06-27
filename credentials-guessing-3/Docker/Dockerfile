FROM alpine:3.7
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \ 
git \
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/credentials-guessing-3
RUN pip3 install -r requirements.txt
CMD [ "python3", "./credentials-guessing-3.py" ]
