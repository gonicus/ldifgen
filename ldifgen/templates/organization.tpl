%amount=9
%contains=organization,locality,organizationalUnit
%force_append=people_container,group_container

dn=%generate_unique_dn(%(base)s,o,%(o)s)f
o=%sn()f
description=%(o)s
objectClass=organization
