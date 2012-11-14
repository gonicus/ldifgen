%amount=9
%contains=organization,locality,organizationalUnit,country
%force_append=people_container,group_container

dn=%generate_unique_dn(%(base)s,o,%(o)s)f
o=%structName()f
ou=%(o)s
description=%(o)s
objectClass=organization
objectClass=gosaDepartment
