%amount=60
%contains=


dn=%generate_unique_dn(%(base)s,%(cn)s)f
sn=%sn()f
givenName=%givenName()f
cn=%(givenName)s %(sn)s
uid=%generate_unique_uid(%(sn)s,%(givenName)s)f
dob=%dob()f
homeDirectory=/home/%(uid)s
userPassword= --Fehlt noch--
gidNumber= --Fehlt noch--
uidNumber= --Fehlt noch--
gecos= %(cn)s
loginShell= /bin/bash
mail= %(uid)s@example.net
homePhone= --Fehlt noch--
telephoneNumber= --Fehlt noch--
objectClass=top
objectClass=person
objectClass=organizationalPerson
objectClass=posixAccount
