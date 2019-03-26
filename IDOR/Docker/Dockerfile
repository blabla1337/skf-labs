FROM alpine:3.7
MAINTAINER Giulio Comi
RUN apk update --no-cache && apk add python3 \
python2-dev \
py2-pip \ 
git 

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/IDOR
RUN pip2 install -r requirements.txt
ENTRYPOINT [ "python2", "./IDOR.py" ]
