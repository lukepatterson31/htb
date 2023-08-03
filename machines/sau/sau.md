# Sau

### Recon

- port 22 SSH OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
- port 80 HTTP filtered
- port 8338 filtered
- port 55555 Request Baskets

hLlzRKwolJugrd2BDI4y8D4MkQtdoqVr6jRilbLQG-4O

### Exploitation

[Exploit PoC](https://github.com/entr0pie/CVE-2023-27163), needs jq installed

Access web server on port 80 and 8338 through SSRF on Request Baskets

`./ssrf-exploit http://10.10.11.224:55555 http://127.0.0.1:8338`

Exploit unauthenticated RCE on Maltrail /login username parameter on port 8338

https://huntr.dev/bounties/be3c5204-fbd9-448d-b97c-96a8d2941e87/


The trick was to base64 encode the payload as shown in [spookier's exploit](https://github.com/spookier/Maltrail-v0.53-Exploit)

### Privilege Escalation

Running sudo -l shows the puma user can run `/usr/bin/systemctl status trail.service` with sudo

We can drop into a root shell by typing `!sh` when told to press RETURN by systemctl
