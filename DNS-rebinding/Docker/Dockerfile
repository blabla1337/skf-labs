FROM alpine:3.7
MAINTAINER Giulio Comi <github.com/giuliocomi>
RUN apk update --no-cache && apk add python3 \
py3-pip \ 
git \
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/DNS-rebinding
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "./rebind.py" ]
