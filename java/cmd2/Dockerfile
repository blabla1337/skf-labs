### STATIC LAYER
FROM openjdk:8-jdk-alpine as builder
LABEL MAINTAINER="Glenn ten Cate <glenn.ten.cate@owasp.org>"

### DYNAMIC LAYER
FROM builder
RUN apk update --no-cache && apk add imagemagick
ARG JAR_FILE=target/*.jar
COPY ${JAR_FILE} /skf/app.jar
ARG STATIC_FILES=target/classes/static
COPY ${STATIC_FILES} /skf/static
ARG TEMPLATES_FILES=target/classes/templates
COPY ${TEMPLATES_FILES} /skf/templates
ARG REPO_FILES=target/classes/repo/bones.png
COPY ${REPO_FILES} /skf/repo/bones.png


### CREATING LIMITED USER AND CHAING WORKDIR FOLDER OWNERSHIP
RUN addgroup -S spring && adduser -S spring -G spring && chown -R spring:spring /skf

### SWITCHING TO THE LIMITED USER
USER spring:spring
WORKDIR /skf
ENTRYPOINT ["java","-jar","app.jar"]
