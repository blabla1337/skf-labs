### Static layers

FROM alpine:3.7 AS skf-alpine37
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

# Installing needed binaries and deps. Then removing unneeded deps:
RUN apk update --no-cache && apk add python3 python3-dev py3-pip bash git

# Needed to fix line endings:
RUN apk add dos2unix --no-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted



### Dynamic layers
FROM skf-alpine37
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN wget https://raw.githubusercontent.com/blabla1337/skf-labs/master/CSRF-weak/requirements.txt \
&& pip3 install --no-cache-dir -r requirements.txt && apk del python3-dev

# Saving space by cloning from Git, then copying only what we need:
RUN cd /tmp && mkdir /skf-labs \
&& git clone https://github.com/blabla1337/skf-labs.git \
&& mv /tmp/skf-labs/CSRF-weak /skf-labs/ \
&& rm -r /tmp/skf-labs && apk del git

# Switching to the new app location:
WORKDIR /skf-labs/CSRF-weak

# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix

# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x

# Starting the actual application:
CMD [ "python3", "./CSRF-weak.py" ]
