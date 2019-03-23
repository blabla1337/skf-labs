FROM alpine:3.7
MAINTAINER Alberto Rafael Rodríguez Iglesias <albertocysec@gmail.com / alberto.iglesias@owasp.org>
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \
git \
bash

RUN git clone https://github.com/AlbertoCoding/skf-labs.git
WORKDIR /skf-labs/AUTH-missing
RUN pip3 install -r requirements.txt
CMD [ "python3", "./Auth-missing.py" ]
