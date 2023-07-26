# Tier 0


### Redeemer

Redis CLI

`redis-cli -h 10.10.10.10 -p 6379`

Redis CLI commands

```
# server info
info

# select DB
select 1

# dump all keys
keys *

# get specific key
get <KEY>
```

### Mongod

MongoDB shell

`mongosh --host 10.10.10.10 --port 27017`

[MongoDB commands](https://www.educative.io/answers/12-basic-mongodb-commands)

```
# list DBs
show dbs

# use DB
use <DB-NAME>

# show DB collections
show collections

# dump collections contents
db.cllection_name.find().pretty()
```

### Rsynced

rsync file transfer and synchronization, works over port 22 or 873

List shares

`rsync rsync://10.10.10.10`

Copy files

`rsync rsync://10.10.10.10/share/file.txt ./file.txt`
