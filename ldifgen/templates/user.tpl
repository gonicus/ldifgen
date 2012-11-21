%amount=60
%contains=


dn=%generate_unique_dn(%(base)s,cn,%(cn)s)f
objectClass=top
objectClass=person
objectClass=organizationalPerson
objectClass=posixAccount
sn=%sn()f
givenName=%givenName()f
cn=%(givenName)s %(sn)s
uid=%generate_unique_uid(sn,givenName)f
dob=%dob()f
homeDirectory=/home/%(uid)s
userPassword=%generate_password()f
gidNumber=1000
uidNumber=%generate_unique_id(uidNumber)f
gecos=%(cn)s
loginShell=/bin/bash
mail=%(uid)s@example.net
homePhone=%generate_phone_number()f
telephoneNumber=%generate_phone_number()f
