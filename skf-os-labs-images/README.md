## Build SKF OS Labs:

Please follow the below instructions to build the base OS image, this contains the Apache Guacamole setup using the LinuxServer.io base image

The last instruction is building the SKF Lab OS image

### docker Base OS image

```
cd skf-os-labs-images
docker build -t blabla1337/owasp-skf-lab:base-v0.1 .
docker push blabla1337/owasp-skf-lab:base-v0.1
```

### docker SKF OS image

```
cd skf-os-labs-images/skf-openbox
docker build -t blabla1337/owasp-skf-lab:hacking-v2-java -f Dockerfile_hacking_java .
docker push blabla1337/owasp-skf-lab:hacking-v2-java
```

Running and testing the SKF OS image:
```
docker run -ti --rm --shm-size=3G --cpus=3 -p 5000:5000 blabla1337/owasp-skf-lab:hacking-v2-java
```

Visit in your browser http://localhost:5000
