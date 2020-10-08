#!/bin/sh

# Setting up firewall nfqueue:
iptables -A INPUT -j NFQUEUE --queue-num 0
#iptables -A PREROUTING -t mangle -m state --state NEW -j CONNMARK --set-mark 1 
#iptables -A PREROUTING -t mangle -m connmark --mark 1 -j NFQUEUE --queue-num 0 

# Starting the interceptor:
python /skf-labs/TLS-downgrade/interceptor.py

