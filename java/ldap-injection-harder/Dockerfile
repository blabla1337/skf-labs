### STATIC LAYER
FROM openjdk:8-jdk-alpine as builder
LABEL MAINTAINER="Glenn ten Cate <glenn.ten.cate@owasp.org>"

### DYNAMIC LAYER
FROM builder
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} /skf/app.jar
COPY glauth /skf/glauth
COPY sample-simple.cfg /skf/sample-simple.cfg
COPY run.sh /skf/run.sh


### CREATING LIMITED USER AND CHAING WORKDIR FOLDER OWNERSHIP
RUN addgroup -S spring && adduser -S spring -G spring && chown -R spring:spring /skf

### SWITCHING TO THE LIMITED USER
USER spring:spring
WORKDIR /skf
RUN chmod +x run.sh && chmod +x glauth

ENTRYPOINT ["/bin/sh", "/skf/run.sh"]
