## Build SKF OS Labs:

Please follow the below instructions to build the base OS image, this contains the Apache Guacamole setup using the LinuxServer.io base image

The last instruction is building the SKF Lab OS image

### docker Base OS image

```
cd skf-os-labs-images
docker build -t blabla1337/owasp-skf-os-labs:base-v0.1 .
docker push blabla1337/owasp-skf-os-labs:base-v0.1
```

### docker SKF OS image

```
cd skf-os-labs-images/skf-openbox
docker build -t blabla1337/owasp-skf-os-labs:python-v0.1 -f Dockerfile_python .
docker push blabla1337/owasp-skf-os-labs:python-v0.1
```

Running and testing the SKF OS image:
```
docker run -ti --rm --shm-size=3G --cpus=3 -p 8080:8080 blabla1337/owasp-skf-os-labs:python-v0.1
```

Visit in your browser http://localhost:8080
