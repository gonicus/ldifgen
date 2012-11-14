%contains=
%amount=0
%max_amount=1

dn=cn=Sample User,%(base)s
objectClass=top
objectClass=person
objectClass=inetOrgPerson
objectClass=organizationalPerson
objectClass=posixAccount
objectClass=gosaAccount
sn=User
givenName=Sample
cn=Sample User
uid=user
homeDirectory=/home/user
userPassword=%generate_password(secret)f
gidNumber=1001
uidNumber=1001
gecos=GOsa Sample user
loginShell=/bin/bash
mail=user@example.net
homePhone=%generate_phone_number()f
telephoneNumber=%generate_phone_number()f
