FROM alpine:3.6
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

# Saving space by cloning from Git, then copying only what we need:
RUN apk update --no-cache && apk add git; cd /tmp && mkdir /skf-labs \
&& git clone https://github.com/blabla1337/skf-labs.git \
&& mv /tmp/skf-labs/TLS-downgrade /skf-labs/ \
&& rm -r /tmp/skf-labs && apk del git


# Switching to the new app location:
WORKDIR /skf-labs/TLS-downgrade


# Needed for the Python web app:
RUN apk update --no-cache && apk add git python python-dev py-pip py-cryptography bash openssl \
iptables gcc g++ libnfnetlink libnfnetlink-dev linux-headers libnetfilter_queue-dev \
&& pip install --no-cache-dir -r requirements.txt && apk del gcc g++ linux-headers py-pip


# Needed to fix line endings:
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted


# Generating a self-signed cert with private key:
RUN openssl genrsa 1024 > /ssl.key && openssl req -new -x509 -nodes -sha1 -days 365 -key /ssl.key -subj "/C=NL/ST=SKF/L=Amsterdam/O=OWASP/CN=localhost" > /ssl.cert


# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix


# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x


# Starting the web app:
CMD [ "python", "./TLS-downgrade.py" ]

