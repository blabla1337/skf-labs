#!/bin/sh

# Setting up firewall nfqueue:
iptables -A FORWARD -j NFQUEUE --queue-num 0

# Starting the interceptor:
python /skf-labs/TLS-downgrade/interceptor.py

