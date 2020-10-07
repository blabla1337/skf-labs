FROM alpine:3.3
MAINTAINER Tess Sluijter-Stek <tsluyter@kilala.nl>

RUN apk update --no-cache && apk add python \
python-dev py-pip py-cryptography \
bash \
openssl

RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted

COPY ./ /skf-labs/TLS-downgrade
WORKDIR /skf-labs/TLS-downgrade

RUN openssl genrsa 1024 > /ssl.key
RUN openssl req -new -x509 -nodes -sha1 -days 365 -key /ssl.key -subj "/C=NL/ST=SKF/L=Amsterdam/O=OWASP/CN=localhost" > /ssl.cert

RUN pip install -r requirements.txt
RUN find . -name "*.py" -exec dos2unix {} \;
RUN find . -name "*.py" -exec chmod +x {} \;

CMD [ "python", "./TLS-downgrade.py" ]