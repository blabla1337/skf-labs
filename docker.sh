#!/bin/bash

#Dirrrty, the way how i like it ^^
for i in $(ls -d */); 
    do 
path=$(pwd)
    dir=${i%%/};
    echo "cd" $dir/Docker"; docker build . -t" $dir "--no-cache; docker push blabla1337/owasp-skf-lab:"$dir"; cd ../.." | tr "[:upper:]" "[:lower:]" 
done

