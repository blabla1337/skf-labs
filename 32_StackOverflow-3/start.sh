#!/bin/bash

#Start SSH server
service ssh start 

# Start webssh
python3 /webssh/run.py 
