#!/bin/bash

# Start apache2
service apache2 restart

# Start the Butterfly terminal
butterfly.server.py --host=0.0.0.0 --unsecure