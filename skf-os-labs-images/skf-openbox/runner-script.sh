#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -l 'python/xss'"
   echo -e "\t-l specify here the language and the lab name"
   echo -e "\t   The lab will be running on localhost:7000"
   echo ""
   echo -e "The available labs to start:"
   echo -e "`ls -r python-labs`"
   echo ""
   exit 1 # Exit script after printing help
}

while getopts "l:" opt
do
   case "$opt" in
      l ) lab_input="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

# Print helpFunction in case parameters are empty
if [ -z "$lab_input" ]
then
   echo "Unknown or incorrect parameter";
   helpFunction
fi

IFS='/'
read -a strarr <<< "$lab_input"

LANGUAGE=${strarr[0]}
LAB=${strarr[1]}

if [ "$LANGUAGE" = "python" ]; then
    cd python-labs/$LAB;
    pip3 install -r requirements.txt
    find . -type f -exec sed -i -e "s,'0.0.0.0','localhost'\, port=7000,g" {} \;
    echo -e "\t   The lab is running on localhost:7000"
    python3 `ls -a | grep .py | grep -v __main__.py | grep -v evil_server.py `
fi

if [ "${strarr[0]}" = "javascript" ]; then
    cd nodeJs-labs/$LAB;
    find app.js -type f -exec sed -i -e "s, 5000, 7000,g" {} \;
    npm install --silent
    echo -e "\t   The lab is running on localhost:7000"    
    node app.js
fi

if [ "${strarr[0]}" = "java" ]; then
    cd java-labs/$LAB;
    find src/main/resources/application.properties -type f -exec sed -i -e "s,port=5000,port=7000,g" {} \; 
    mvn package -Dmaven.test.skip=true
    echo -e "\t   The lab is running on localhost:7000"
    java -jar target/app.jar
fi