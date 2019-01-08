FROM alpine:3.7
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>
RUN apk update --no-cache && apk add python3 \
python3-dev \
py3-pip \ 
git

#RUN apt-get install -y git python-pip python-dev build-essential
#RUN pip install -r requirements.txt
RUN git clone https://github.com/blabla1337/skf-labs.git
WORKDIR /skf-labs/LFI
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD [ "python3", "./LFI.py" ]