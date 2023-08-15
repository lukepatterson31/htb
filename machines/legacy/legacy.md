# Legacy

- port 135/tcp msrpc Microsoft Windows RPC
- port 139/tcp netbios-ssn Microsoft Windows netbios-ssn
- port 445/tcp microsoft-ds Windows XP microsoft-ds

OS: Windows, Windows XP; CPE: cpe:/o:microsoft:windows, cpe:/o:microsoft:windows_xp

Running nmap script smb-vuln-ms08-067 shows the tagret is vulnerable to the MS 08-067 Netapi exploit

### Exploitation

Run metsasploit exploit windows/smb/ms08_067_netapi to gain a root shell
