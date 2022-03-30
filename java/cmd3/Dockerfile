### STATIC LAYER
FROM openjdk:8-jdk-alpine as builder
LABEL MAINTAINER="Glenn ten Cate <glenn.ten.cate@owasp.org>"
RUN  apk add maven


### DYNAMIC LAYER
FROM builder
RUN apk update --no-cache && apk add imagemagick
COPY src/ /skf/src/
COPY pom.xml /skf/
ARG STATIC_FILES=src/main/resources/static
COPY ${STATIC_FILES} /skf/static
ARG TEMPLATES_FILES=src/main/resources/templates
COPY ${TEMPLATES_FILES} /skf/templates
ARG REPO_FILES=src/main/resources/static/img/bones.png
COPY ${REPO_FILES} /skf/repo/bones.png


### CREATING LIMITED USER AND CHAING WORKDIR FOLDER OWNERSHIP
RUN addgroup -S spring && adduser -S spring -G spring && chown -R spring:spring /skf

### SWITCHING TO THE LIMITED USER
USER spring:spring
WORKDIR /skf
RUN mvn package -Dmaven.test.skip=true

ENTRYPOINT ["java","-jar","/skf/target/app.jar"]
