# MonitorsTwo

### Reconnaissance

- port 22 SSH OpenSSH 8.2p1 Ubuntu 4ubuntu0.5 (Ubuntu Linux; protocol 2.0)
- port 80 HTTP nginx 1.18.0 (Ubuntu)

port 80 is running Cacti v 1.2.22 which is vulnerable to an [RCE attack](https://github.com/FredBrave/CVE-2022-46169-CACTI-1.2.22)

### Exploitation

Run exploit to gain a reverse shell as www-data

Running inside a docker container, /sbin/capsh has SUID set allowing privesc to root inside the container

`/sbin/capsh --gid=0 --uid=0 --`

The entrypoint script contains sql credentials for the db containing password hashes.

Crack marcus' hash and ssh into the machine, escaping the docker container

marcus:funkymonkey

Services running on 127.0.0.1:39335 and 127.0.0.1:8080

### Privilege Escalation

On login as marcus a notfication tells us we have mail

Running `find / -type d -name mail 2>/dev/null` shows a mail directory which contains an email from security 
advising various vulnerabilities be patched. 

[CVE-2021-41091](https://github.com/UncleJ4ck/CVE-2021-41091) grants us root access after setting the suid 
bit on /bin/bash in the docker container

Docker container:

`# chmod +s /bin/bash`

Host:

```
./poc.sh

# navigate to path shown in output of poc.sh
./bin/bash -p
```
