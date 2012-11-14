%amount=9
%contains=organization,locality,organizationalUnit
%force_append=people_container,group_container

dn=%generate_unique_dn(%(base)s,ou,%(ou)s)f
ou=%structName()f
description=%(ou)s
objectClass=organizationalUnit
