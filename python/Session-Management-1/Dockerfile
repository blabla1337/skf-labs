### Static layers

FROM python:3.7-alpine AS skf-alpine37
LABEL Glenn ten Cate <glenn.ten.cate@owasp.org>

# Installing needed binaries and deps. Then removing unneeded deps:
RUN apk update --no-cache && apk add py3-pip bash dos2unix

### Dynamic layers
FROM skf-alpine37
LABEL Glenn ten Cate <glenn.ten.cate@owasp.org>

RUN addgroup -g 1000 app 
RUN adduser -u 1000 -G app -D -h /home/app app
RUN rm -rf /var/cache/apk/APKINDEX*

COPY ./ /home/app/Session-Management-1

# Switching to the new app location:
WORKDIR /home/app/Session-Management-1

RUN chown -R app:app /home/app/Session-Management-1

# Switching to the limited user
USER app

# Installing needed binaries and deps
RUN pip3 install --no-cache-dir --user -r requirements.txt 

# Fixing Windows line endings for our students:
RUN find . -name "*.sh" -o -name "*.py" -o -name "*.css" -o -name "*.js" | xargs dos2unix

# Setting chmod +x on the scripts:
RUN find . -name "*.sh" -o -name "*.py" | xargs chmod +x

# Starting the actual application:
ENTRYPOINT [ "python3", "./Session-Management-1.py" ]

