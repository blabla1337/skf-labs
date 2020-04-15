FROM alpine:3.7
MAINTAINER Giulio Comi
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \ 
git 

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/IDOR
RUN pip3 install -r requirements.txt
ENTRYPOINT [ "python3", "./IDOR.py" ]
