FROM alpine:3.7 AS cors-build
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

# Saving space by cloning from Git, then copying only what we need:
RUN apk update --no-cache && apk add git; cd /tmp && mkdir /skf-labs \
&& git clone https://github.com/blabla1337/skf-labs.git \
&& mv /tmp/skf-labs/CORS /skf-labs/ \
&& rm -r /tmp/skf-labs && apk del git

# Switching to the new app location:
WORKDIR /skf-labs/CORS

# Installing needed binaries and deps. Then removing unneeded deps:
RUN apk update --no-cache && apk add python3 python3-dev py3-pip bash \
&& pip3 install -r requirements.txt && apk del python3-dev

# Needed to fix line endings:
RUN apk add dos2unix --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/community/ --allow-untrusted

# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix

# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x

# Starting the actual application:
CMD [ "python3", "./CORS.py" ]



# Reducing all the layers down to one:
FROM cors-build
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>
