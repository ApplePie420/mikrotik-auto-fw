# MikroTik auto-fw
## About
I work as a systems administrator for a major hosting company. We have quite a bit of issues with different attacks, be it common wordpress attack vectors (xmlrpc, wp-login, authors, database) or just plain DoS/DDoS attacks, or any other (port probing, form spam, SSH or FTP attacks and many, many more), we have it. Over the time, I've compiled a list of IP ranges or companies, that usually cause the most trouble. 

Since I use MikroTik devices exclusively (because they are awesome!), and I host some services on my home network myself, they are (unfortunately) being exposed to these attacks. I've decicided to create this collection of scripts that will automatically update my router's firewall rules based on some iplists and settings I provide. Since the premise of all of this is expandability and modularity, you can decide which services and networks to block. You can select from curated, pre-compiled lists of known subnets that cause troubles, or specify your own. If you don't want to just block, but have lots of IP addresses or IP ranges, this script can also be used to simply manage your MikroTik's firewall rules by a script.

## Usage
TBA