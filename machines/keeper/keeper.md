# Keeper

### Reconnaissance

- port 22 SSH OpenSSH 8.9p1 Ubuntu 3ubuntu0.3 (Ubuntu Linux; protocol 2.0)
- port 80 HTTP nginx 1.18.0 (Ubuntu)

Default credentials log us in as root to the RT panel

OS: Ubuntu 22.04
uname -a: Linux keeper 5.15.0-78-generic #85-Ubuntu SMP Fri Jul 7 15:25:09 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux


### Exploitation 

SSH credentials found in an RT user's information

Found a zip file containing a .kdbx file and the KeePass dump mentioned in the tickets on RT in the user's 
home dir

### Privilege Escalation

KeePass 2.X is vulnerable to typed master password extraction from pagefile/swapfile, hibernation file and 
crash dumps. [CVE-2023-32784 PoC by vdohney](https://github.com/vdohney/keepass-password-dumper) and some 
Googling of the results gives us the password for the .kdbx file and root access through a puTTy ssh key
