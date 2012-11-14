%amount=5
%contains=locality,organization,organizationalUnit

dn=%generate_unique_dn(%(base)s,c,%(c)s)f
c=%structName()f
ou=%(c)s
description=%(c)s
objectClass=country
objectClass=top
objectClass=gosaDepartment
