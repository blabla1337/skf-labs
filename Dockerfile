FROM codercom/code-server:3.8.0
MAINTAINER Glenn ten Cate <glenn.ten.cate@owasp.org>

USER root

RUN apt-get update && apt-get install -y python3 \
python3-dev \
python3-pip \ 
git

USER coder

COPY --chown=coder:coder . /skf-labs
WORKDIR /skf-labs

# Lets do a test run with pip3 to verify its working
RUN pip3 install -r SQLI/requirements.txt

RUN mkdir -p ~/.config/code-server/
RUN echo "bind-addr: 127.0.0.1:8080" > ~/.config/code-server/config.yaml
RUN echo "auth: password" >> ~/.config/code-server/config.yaml
RUN echo "password: skf-labs" >> ~/.config/code-server/config.yaml
RUN echo "cert: false" >> ~/.config/code-server/config.yaml

CMD [ "code-server", "/skf-labs" ]

