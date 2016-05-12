#!/usr/bin/python2

import sys, os, xmpp, time, select, socket, subprocess
from ctypes import c_char_p
from subprocess import call

# this is not an xmpp server
# only a simple tcp server that would server as a reverse shell interface
# or receive a pcap dump and analyze it

def get_http_headers(payload):
    try:
        headers_raw = payload[:payload.index("\r\n\r\n")+2]
        headers = dict(re.findall(r'(?P<name>.*?):(?P<value>.*?)\r\n', headers_raw))
    except:
        return None
    if 'Content-Type' not in headers:
        return None
    return headers

def pcap_http_dump(pcap_fn, dump_fn):
    fd = open('%s' % (dump_fn), 'a+')
    p = rdpcap(pcap_fn)
    sessions = p.sessions()
    payload = [] # init http data cotainer
    # follow and dump every http transmission in the pcap
    for s in sessions: # this is equivalent to following packets in wireshark
        curr_payload = ''
        for packet in sessions[s]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80: # check if the transmission is http
                    curr_payload += str(packet[TCP].payload)
            except:
                pass
            headers = get_http_headers(payload)
            if headers is None:
                continue
        	# dump the packet
            fd.write(curr_payload)
    fd.close()

if __name__ == '__main__':
	port = 3030 # arbitrary
	s = socket.socket()
	host = socket.gethostname()
	s.bind((host, port))
	s.listen(5)

	i = 0	

	while True:
	    conn, addr = s.accept()
	    # print 'connection from', addr
	    data = conn.recv(4)

	    if data[0:4] == 'PCAP':
		    pcap_fn = 'dump.pcap' + str(i)
		    i = i + 1
		    f = open(pcap_fn, 'a+')
		    while True:
	        	# print('receiving data...')
	        	data = conn.recv(1024)
	        	# print('data: %s', (data))
	   	    	if not data:
				break
	        	# write data to a file
	        	f.write(data)
		    f.close()
		    if data[0:4] == 'SHLL':
			call(["nc", "-lvp", str(port)]) # use the terminal as reverse shell interface

	conn.close()


