# crak

A password file dictionary based password cracker

## requirements

1. linux shadow password file containing passwords to attack
2. file containing word dictionary.

## usage

### installation

`pip install crak`

### help

```
crak -h
usage: crak [-h] [--version] [-d WORDDICT] [-u USERNAME] shadowfile

Perform a dictionary crack on a list of encrypted passwords using a wordlist

positional arguments:
  shadowfile            Shadow password file containing crypted passwords

optional arguments:
  -h, --help            show this help message and exit
  --version             prints version information
  -d WORDDICT, --worddict WORDDICT
                        Word dictionary files to use in attack
  -u USERNAME, --username USERNAME
                        specific username - if not defined then all users in
                        shadow file will be attempted
```

### list users

will list all valid users in the shadow file and is useful to see what username to target specifically

```
crak shadow 

-=( crak v 0.0.1 )=-

list of usernames in shadow file
                                                        password
username                                                        
root           $6$QlJt0cnr$hmgN/fzUrHFFI1SaGXVNzE060TPuwsZdzP...
backup         $6$Tye3KuC5$rVIT3u5M9IhZZI.jRanteGT3o7DbkLFWb/...
allison        $6$sPsSvR2J$wk59pi4or6QR5IobArTZpn4k7i2jZQ07pY...
paul           $6$YGG4oFLp$avrVGY6.S59aApmCY/60A7AWfGDBh/zI7L...
dr_balustrade  $6$3kgge6ym$OcIOZS8bJy41YsLYXToOW2Ag3imG1KEXkP...
```

### dictionary attack all users

will run a dictionary attack against all the valid users in the shadow file

```
crak shadow -d dicttest.txt

-=( crak.py v 0.0.1 )=-

starting to crack passwords for all users
No password found: root
No password found: backup
No password found: allison
No password found: paul
*** FOUND PASSWORD ***
Username: dr_balustrade
Password: pinky
**********************
```

### Specify user to perform brute force attack on

Will target a specific user

```
crak shadow -d dicttest.txt -u dr_balustrade

-=( crak v 0.0.1 )=-

starting to crack password for user: dr_balustrade
*** FOUND PASSWORD ***
Username: dr_balustrade
Password: pinky
**********************
```

### Display version

displays the current version

```
crak --version
crak v0.0.1
```
