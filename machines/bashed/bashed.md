# Bashed

### Reconnaissance

- port 80/tcp HTTP Apache httpd 2.4.18 ((Ubuntu))

Gobuster scan reveals a /dev directory containing phpbash allowing RCE on the target

`gobuster dir -u http://10.10.10.68 -w /usr/share/wordlists/dirb/common.txt`

### Exploitation

Upload a meterpreter shell to the target throught the phpbash webshell

### Privilege Escalation

Target OS version Ubuntu 16.04 running kernel version 4.4.x is vulnerable to privilege escalation using 
an [adaptation of CVE-2017-16995](https://ricklarabee.blogspot.com/2018/07/ebpf-and-analysis-of-get-rekt-linux.html) giving us root

*Official method:*

www-data can run any command as user scriptmanager allowing access to the /scripts directory

There is a python script test.py which updates a txt file owned by root in the /scripts directory every minute

We can modify the script to send a reverse shell to the attacking machine giving us root
