# Netmon

### Reconnaissance

- 21/tcp ftp Microsoft ftpd
- 80/tcp HTTP Indy httpd 18.1.37.13946 (Paessler PRTG bandwidth monitor)
- 135/tcp msrpc Microsoft Windows RPC
- 139/tcp netbios-ssn  Microsoft Windows netbios-ssn
- 445/tcp microsoft-ds Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
- 5985/tcp Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
- 47001/tcp Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)

SMB requires login but FTP anonymous access is enabled

FTP contains C:\ allowing direct access to user.txt

In PRTG config files an old DB password is visible containing a date, incrementing the date gives us access 
to the admin panel

### Exploitation

The version of PRTG installed is vulnerable to RCE through the notification service in Settings

### Privilege Escalation

PRTG is running as Administrator granting us access to root.txt
