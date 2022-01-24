#!/bin/bash

SERVICE="stack-overflow"
PORT1=10007
PORT2=10003

sudo docker kill $SERVICE
sudo docker rm $SERVICE

sudo docker build -t $SERVICE . && sudo docker run -dt -p $PORT1:8888 -p $PORT2:22 --name $SERVICE $SERVICE
