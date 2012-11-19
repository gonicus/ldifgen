%amount=0
%contains=organization,location


dn=%generate_unique_dn(%(base)s,%(dc)s)f
dc=%sn()f
o=%(dc)s
ou=%(dc)s
description=%(dn)s
objectClass=dcObject
objectClass=organization
