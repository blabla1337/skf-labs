FROM ubuntu:latest
MAINTAINER Abhishek "abhiabhi2306@gmail.com"
RUN apk update --no-cache && apk add git \
python2-dev \
py2-pip \ 
git \
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/ratelimiting
RUN pip install -r requirements.txt
CMD [ "python2", "./ratelimiting.py" ]