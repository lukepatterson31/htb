# Arctic

### Reconnaissance

- port 135/tcp RPC
- port 8500/tcp ColdFusion
- port 49154/tcp RPC

port 135 can be used to enumerate available services: [RPC dump](./arctic.rpcdump)

port 8500 resolves to a directory listing of a ColdFusion server

Poking around in the directories we can see the administrator panel, which shows the target is running 
ColdFusion 8

ColdFusion 8 is vulnerable to RCE, CVE-2009-2265 - [exploit-db](https://www.exploit-db.com/exploits/50057)

### Exploitation

Set variables in exploit 50057.py and run, giving us RCE on the target

`python3 50057.py`

Running winPEASx64.exe didn't work, the command was just echoed back

Windows Exploit Suggester and Windows Exploit Suggester Next-Generation [show multiple privesc vulnerabilities](./arctic-exploits.md)

We can use msfconsole's exploit/multi/script/web_delivery module to get a reverse meterpreter shell and run 
local exploit suggester to see the target is vulnerable to multiple privilege escalation modules

### Privilege Escalation

Run windows/local/ms10_092_schelevator to gain a reverse shell as NT Authority\System
Also vulnerable to MS10-059 (Chimmichurri)

**To Do**
- add pictures of discovery
- non-Metasploit privesc