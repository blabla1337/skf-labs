FROM alpine:3.7
MAINTAINER Davide Cioccia <d.cioccia@dcodx.com>
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \ 
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/graphql-introspection

RUN pip3 install -r requirements.txt 
RUN python3 populate-database.py
CMD [ "python3", "app.py"]