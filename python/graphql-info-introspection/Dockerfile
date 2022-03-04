### Static layers

FROM alpine:3.7 AS skf-alpine37
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

# Installing needed binaries and deps. Then removing unneeded deps:
RUN apk update --no-cache && apk add python3 \
  python3-dev \
  py3-pip \
  bash \
  git \
  dos2unix \
  build-base \
  gcc \
  musl-dev \
  g++

### Dynamic layers
FROM skf-alpine37
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN addgroup -g 1000 app 
RUN adduser -u 1000 -G app -D -h /home/app app
RUN rm -rf /var/cache/apk/APKINDEX*

COPY ./ /home/app/graphql-info-introspection

# Switching to the new app location:
WORKDIR /home/app/graphql-info-introspection

RUN chown -R app:app /home/app/graphql-info-introspection

# Switching to the limited user
USER app

# Installing needed binaries and deps
RUN pip3 install --no-cache-dir  --user -r requirements.txt 

# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix

# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x

# Populate data from file
RUN python3 populate-database.py

# Starting the actual application:
ENTRYPOINT [ "python3", "./app.py" ]
