FROM alpine:3.7
MAINTAINER Davide Cioccia
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \ 
git \
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/Url-redirection-harder2
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "./redirect.py" ]
