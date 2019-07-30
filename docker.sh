#!/bin/bash

#Dirrrty, the way how i like it ^^
for i in $(ls -d */); 
    do 
    dir=${i%%/};
    echo "cd" $dir/Docker"; docker build . -t blabla1337/owasp-skf-lab:"$dir "--no-cache; docker push blabla1337/owasp-skf-lab:"$dir"; cd ../.." | tr "[:upper:]" "[:lower:]" 
done

