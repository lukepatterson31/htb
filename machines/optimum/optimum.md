# Optimum

### Reconnaissance

- port 80/tcp HTTP HttpFileServer httpd 2.3

### Exploitation

Rejetto HFS is [vulnerable to RCE](https://www.exploit-db.com/exploits/39161) through a file upload

Change the IP and port variables in the exploit file, host nc.exe on port 80 and start a listener on 
whichever port you set in the exploit file. Run the exploit to gain a remote shell on the target

### Privilege Escalation

Upload a meterpreter shell with certutil and migrate to a stable x64 process like explorer.exe

Winpeas shows the target was potentially vulnerable to handle based privesc

Running `multi/recon/local_exploit_suggester` in metasploit shows that the target is vulnerable to 
`exploit/windows/local/ms16_032_secondary_logon_handle_privesc` giving us a system shell and root.txt
