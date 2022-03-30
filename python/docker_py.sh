#!/bin/bash

#Dirrrty, the way how i like it ^^
for i in $(ls -d */); 
    do 
    dir=${i%%/};
    echo "docker login; cd" $dir"; docker buildx build --platform linux/amd64,linux/arm/v7 -t blabla1337/owasp-skf-lab:"$dir " --push .; cd .." | tr "[:upper:]" "[:lower:]" 
done

# one print for the Visual Studio Code web version that has the labs included
#echo "buildx build -f Dockerfile  --platform linux/amd64 -t blabla1337/owasp-skf-lab:vs-code --push ."
