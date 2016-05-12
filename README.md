# Botnet

This is the final project for CS 460 Spring 2016. Team is just me: Zhaoli Wen (zwen6). 

Botnet is some Python scripts that has some basic features of some malware. It is an extension of the fourth lab, which is a bot that uses victim machines as zombies and do the master server's bidding. I have added the functionalities of: 

  - DDoS attack a given host and port
  - Sniff the traffic on the victim and send back the pcap dump file to a given host
  - Open up a reverse shell back to a given host

The Python server is also included in the repo. To use it, one needs a Jabba server and to modify some parameters in the scripts. 
