#!/bin/bash

#Dirrrty, the way how i like it ^^
for i in $(ls -d */); 
    do 
    dir=${i%%/};
    #echo "cd" $dir/Docker"; docker buildx build --platform linux/amd64,linux/arm/v7 --no-cache -t blabla1337/owasp-skf-lab:"$dir " --push .; cd ../.." | tr "[:upper:]" "[:lower:]" 
    echo "docker login; cd" $dir/Docker"; docker buildx build --platform linux/amd64,linux/arm/v7 -t blabla1337/owasp-skf-lab:"$dir " --push .; cd ../.." | tr "[:upper:]" "[:lower:]" 
done

