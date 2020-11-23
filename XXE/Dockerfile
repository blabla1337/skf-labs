### Static layers

FROM alpine:3.7 AS skf-alpine37-py27
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

# Installing needed binaries and deps. Then removing unneeded deps:
RUN apk update --no-cache && apk add python2-dev \
python2-dev \
py2-pip \ 
gcc \
linux-headers \
libc-dev \
openldap-dev \
git \
dos2unix

### Dynamic layers
FROM skf-alpine37-py27
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN addgroup -g 1000 app 
RUN adduser -u 1000 -G app -D -h /home/app app
RUN rm -rf /var/cache/apk/APKINDEX*

COPY ./ /home/app/XXE

# Switching to the new app location:
WORKDIR /home/app/XXE

RUN chown -R app:app /home/app/XXE

# Switching to the limited user
USER app

# Installing needed binaries and deps
RUN pip install --no-cache-dir  --user -r requirements.txt 

# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix

# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x

# Starting the actual application:
ENTRYPOINT [ "python2", "./XXE.py" ]
