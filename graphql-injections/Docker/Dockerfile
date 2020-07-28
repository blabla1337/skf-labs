FROM alpine:3.7
MAINTAINER Stefan Petrushevski <stefan@zeroscience.mk>
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \ 
git \
bash

RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/graphql-injections

RUN pip3 install -r requirements.txt 
#RUN python3 populate-database.py
CMD [ "python3", "app.py"]