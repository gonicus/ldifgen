%amount=60
%contains=


dn=%generate_unique_dn(%(base)s,%(cn)s)f
sn=%sn()f
givenName=%givenName()f
cn=%(givenName)s %(sn)s
uid=%generate_unique_uid(%(sn)s,%(givenName)s)f
dob=%dob()f
objectClass=top
objectClass=person
objectClass=organizationalPerson
objectClass=gosaAccount
