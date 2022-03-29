### STATIC LAYER
FROM openjdk:8-jdk-alpine as builder
LABEL MAINTAINER="Glenn ten Cate <glenn.ten.cate@owasp.org>"

### DYNAMIC LAYER
FROM builder
ARG RES=text
COPY ${RES} /skf/text
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} /skf/app.jar

### CREATING LIMITED USER AND CHAING WORKDIR FOLDER OWNERSHIP
RUN addgroup -S spring && adduser -S spring -G spring && chown -R spring:spring /skf

### SWITCHING TO THE LIMITED USER
USER spring:spring
WORKDIR /skf

ENTRYPOINT ["java","-jar","app.jar"]
