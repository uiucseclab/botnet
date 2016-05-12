# Botnet

This is the final project for CS 460 Spring 2016. Team is just me: Zhaoli Wen (zwen6). 

Botnet is some Python scripts that has some basic features of some malware. It is an extension of the fourth lab, which is a bot that uses victim machines as zombies and do the master server's bidding. I have added the functionalities of: 

  - DDoS attack a given host and port
  - Sniff the traffic on the victim and send back the pcap dump file to a given host
  - Open up a reverse shell back to a given host

The Python server is also included in the repo. To use it, one needs a Jabba server and to modify some parameters in the scripts. 

To test, open up any XMPP client and use it to buddy the running python bot. And use the following format to send commands: 

  - PCAP[host]:[port]
  - SHLL[host]:[port]
  - DDOS[host]:[port]

where PCAP tells the bot to intercept and dump up to 1024 TCP packets on the zombie and dump to a pcap file, and send it back to the master, SHLL opens up a reverse shell back to the master. For the above 2 commands the host and port are of the master's. DDOS tells the bot to try to overload some victim server on a port. 

Don't forget to start up the bot master on your own machine. The bot master is a simple TCP server waiting for any replies from any bots. It would write the pcap file or act as a shell interface to the zombie. 
