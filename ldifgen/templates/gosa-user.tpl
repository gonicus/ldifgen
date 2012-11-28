%amount=60
%contains=


dn=%generate_unique_dn(%(base)s,cn,%(cn)s)f
objectClass=top
objectClass=person
objectClass=inetOrgPerson
objectClass=organizationalPerson
objectClass=posixAccount
objectClass=gosaAccount
sn=%sn()f
givenName=%givenName()f
cn=%(givenName)s %(sn)s
uid=%generate_unique_uid(sn,givenName)f
homeDirectory=/home/%(uid)s
userPassword=%generate_password()f
dob=%dob()f
gidNumber=1000
uidNumber=%generate_unique_id(uidNumber)f
gecos=%(uid)s
loginShell=/bin/bash
mail=%(uid)s@example.net
homePhone=%generate_phone_number()f
telephoneNumber=%generate_phone_number()f
