FROM alpine:3.3
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>


# Needed for the Python web app:
RUN apk update --no-cache && apk add python \
python-dev py-pip py-cryptography \
bash \
openssl


# Needed for the interceptor:
RUN apk add iptables tcpdump gcc g++ libnfnetlink libnfnetlink-dev linux-headers libnetfilter_queue-dev

# Needed to fix line endings:
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted


# Setting up the application and installing more dependencies:
COPY ./ /skf-labs/TLS-downgrade
WORKDIR /skf-labs/TLS-downgrade
RUN pip install -r requirements.txt


# Cleaning up packages that were only for the build:
RUN apk del gcc g++ linux-headers


# Generating a self-signed cert with private key:
RUN openssl genrsa 1024 > /ssl.key
RUN openssl req -new -x509 -nodes -sha1 -days 365 -key /ssl.key -subj "/C=NL/ST=SKF/L=Amsterdam/O=OWASP/CN=localhost" > /ssl.cert


# Fixing Windows line endings for our students:
RUN find . -name "*.py" -exec dos2unix {} \;
RUN find . -name "*.css" -exec dos2unix {} \;
RUN find . -name "*.js" -exec dos2unix {} \;


# Starting the web app:
RUN find . -name "*.sh" -exec chmod +x {} \;
RUN find . -name "*.py" -exec chmod +x {} \;
CMD [ "python", "./TLS-downgrade.py" ]