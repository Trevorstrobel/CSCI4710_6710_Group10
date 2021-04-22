//Authors:          Trevor Strobel
//Date:             4/22/21


---
MemeMaker DB Generation
---


This document describes the process of (re)creating the database and tables used in
MemeMaker. This document assumes that you've already installed PostgreSQL on your linux
system. 

<h4>Database Creation</h4>

```
$ sudo -u postgres psql 
```
You will now see your prompt with the prefix ```postgres=#``` 
Note here, that each line ends with ```;```
sudo -r
First we create the databse:
```
create database mememaker;
```

Then we create a user:
```
create user mmadmin with encrypted password 'csci4710';
```

Then we grant privileges to that user:
```
grant all privileges on database mememaker to mmadmin;
```

Finally, we quit ```psql```:
```
\q 
```

You should now be back at your shell, indicated by the ```$ ``` character in Bash.

