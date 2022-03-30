### STATIC LAYER
FROM openjdk:8-jdk-alpine as builder
LABEL MAINTAINER="Glenn ten Cate <glenn.ten.cate@owasp.org>"
RUN  apk add maven


### DYNAMIC LAYER
FROM builder
COPY src/ /skf/src/
COPY pom.xml /skf/

### CREATING LIMITED USER AND CHAING WORKDIR FOLDER OWNERSHIP
RUN addgroup -S spring && adduser -S spring -G spring && chown -R spring:spring /skf

### SWITCHING TO THE LIMITED USER
USER spring:spring
WORKDIR /skf
RUN mvn package -Dmaven.test.skip=true

ENTRYPOINT ["java","-jar","/skf/target/app.jar"]
