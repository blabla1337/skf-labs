### STATIC LAYER
FROM openjdk:8-jdk-alpine as builder
LABEL MAINTAINER="Glenn ten Cate <glenn.ten.cate@owasp.org>"
RUN  apk add maven


### DYNAMIC LAYER
FROM builder
COPY src/ /skf/src/
COPY pom.xml /skf/
COPY glauth /skf/glauth
COPY sample-simple.cfg /skf/sample-simple.cfg
COPY run_services.sh /skf/run_services.sh


### CREATING LIMITED USER AND CHAING WORKDIR FOLDER OWNERSHIP
RUN addgroup -S spring && adduser -S spring -G spring && chown -R spring:spring /skf

### SWITCHING TO THE LIMITED USER
USER spring:spring
WORKDIR /skf
RUN chmod +x run_services.sh && chmod +x glauth
RUN mvn package -Dmaven.test.skip=true

ENTRYPOINT ["java","-jar","/skf/target/app.jar"]
