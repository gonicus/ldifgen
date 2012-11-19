%amount=9
%contains=organization,location
%force_append=people_container,group_container


dn=%generate_unique_dn(%(base)s,%(o)s)f
o=%sn()f
ou=%(o)s
description=%(o)s
objectClass=dcObject
objectClass=organization
