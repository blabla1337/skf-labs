FROM alpine:3.7
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>
RUN apk update --no-cache && apk add python3 \
python2-dev \
py3-pip \ 
git \
bash

RUN git clone https://github.com/giuliocomi/skf-labs.git
WORKDIR /skf-labs/SSRF
RUN pip3 install -r requirements.txt
CMD [ "python2", "./SSRF.py" ]
