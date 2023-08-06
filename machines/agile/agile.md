# Agile

### Reconnaissance 

- port 22 SSH OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
- port 80 HTTP nginx 1.18.0 (Ubuntu)

domain superpass.htb

Wappalyzer scan

"URL":						"http://superpass.htb"
"Miscellaneous":			"Popper"
"Web servers":				"Nginx"
"Operating systems": 		"Ubuntu"
"JavaScript libraries": 	"jQuery ; \_hyperscript  ; Htmx"
"Reverse proxies": 			"Nginx"
"UI frameworks": 			"Bootstrap"

/register as admin causes SQL operational error, dislcosing python backend and db tables

```
sqlalchemy.exc.OperationalError: (pymysql.err.OperationalError) (2013, 'Lost connection to MySQL server during query')
[SQL: SELECT users.id AS users_id, users.username AS users_username, users.hashed_password AS users_hashed_password 
FROM users 
WHERE users.username = %(username_1)s 
 LIMIT %(param_1)s]
[parameters: {'username_1': 'admin', 'param_1': 1}]
(Background on this error at: https://sqlalche.me/e/14/e3q8)
```

interactive python shell available, pin locked

error page shows 2 page sources, /vault with export and add-password functionalty visible

No subdomains found

Registered as a user, added passwords and exported the vault but was stuck after that.

Looked at [this walkthrough](https://medium.com/@amitth/hackthebox-agile-machine-walkthrough-1a774964d773) and used the LFI to download /etc/passwd

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
usbmux:x:107:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
corum:x:1000:1000:corum:/home/corum:/bin/bash
dnsmasq:x:108:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
mysql:x:109:112:MySQL Server,,,:/nonexistent:/bin/false
runner:x:1001:1001::/app/app-testing/:/bin/sh
edwards:x:1002:1002::/home/edwards:/bin/bash
dev_admin:x:1003:1003::/home/dev_admin:/bin/bash
_laurel:x:999:999::/var/log/laurel:/bin/false
```

Used LFI to read /proc/self/environ containing envrionment variables

```
LANG=C.UTF-8.
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin.
HOME=/var/www.
LOGNAME=www-data.
USER=www-data.
INVOCATION_ID=74df27ea238d4aeda94f093e87b9780f.
JOURNAL_STREAM=8:32552.
SYSTEMD_EXEC_PID=1072.
CONFIG_PATH=/app/config_prod.json.
```

Config contains SQL URI and credentials, unfortunately locally hosted

`"SQL_URI": "mysql+pymysql://superpassuser:dSA6l7q*yIVs$39Ml6ywvgK@localhost/superpass"`

corum, edwards, and dev_admin home dirs contain ssh key id_rsa but no access through LFI

### Exploitation
