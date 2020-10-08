#!/usr/bin/python
#
# With many thanks to Ludovic Barman for their great write-up.
# https://lbarman.ch/blog/downgrade-tls/
#
# Also, @XargsNotBombs makes the wonderful Illustrated TLS Connections site.
# https://tls.ulfheim.net
#

from netfilterqueue import NetfilterQueue
from scapy import *

scapy_builtins = __import__('scapy.all', globals(), locals(),'.').__dict__
__builtins__.__dict__.update(scapy_builtins)

nfQueueID         = 0
maxPacketsToStore = 100

def packetReceived(pkt):             # called each time a packet is put in the queue
  print("New packet received.")
  pkt.accept();                      # accepts and forwards this packet to the appropriate network address

print("Binding to NFQUEUE", nfQueueID)
nfqueue = NetfilterQueue()
nfqueue.bind(nfQueueID, packetReceived, maxPacketsToStore) # binds to queue 0, use handler "packetReceived()"
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('Listener killed.')

nfqueue.unbind()

