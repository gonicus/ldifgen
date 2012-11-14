%contains=
%amount=0
%max_amount=1

dn=cn=GOsa Administrator,%(base)s
objectClass=top
objectClass=person
objectClass=inetOrgPerson
objectClass=organizationalPerson
objectClass=posixAccount
objectClass=gosaAccount
sn=Administrator
givenName=GOsa
cn=GOsa Administrator
uid=admin
homeDirectory=/home/admin
userPassword=%generate_password(tester)f
gidNumber=1000
uidNumber=1000
gecos=GOsa Administrator
loginShell=/bin/bash
mail=admin@example.net
homePhone=%generate_phone_number()f
telephoneNumber=%generate_phone_number()f
