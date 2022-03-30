#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -l 'python/xss'"
   echo -e "\t-l specify here the language and the lab name"
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
    python3 `ls -a | grep .py | grep -v __main__.py | grep -v evil_server.py `
fi

if [ "${strarr[0]}" = "javascript" ]; then
    cd nodeJs-labs/$LAB;
    npm install --silent
    node app.js
fi

if [ "${strarr[0]}" = "java" ]; then
    cd java-labs/$LAB;
    mvn package -Dmaven.test.skip=true
    java -jar target/app.jar
fi