# Blue

### Reconnaissance

- port 135/tcp MSRPC
- port 139/tcp NetBIOS
- port 445/tcp SMB Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
- port 49152/tcp MSRPC
- port 49153/tcp MSRPC
- port 49154/tcp MSRPC
- port 49155/tcp MSRPC
- port 49156/tcp MSRPC
- port 49157/tcp MSRPC

Nmap script smb-vuln-ms17-010.nse shows target is vulnerable to MS 17-010

### Exploitation

Run Eternal Romance from metasploit to gain root access

