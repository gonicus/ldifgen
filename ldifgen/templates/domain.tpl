%amount=0
%contains=organization,locality,organizationalUnit


dn=%generate_unique_dn(%(base)s,dc,%(dc)s)f
dc=%sn()f
o=%(dc)s
ou=%(dc)s
description=%(dn)s
objectClass=dcObject
objectClass=organization
