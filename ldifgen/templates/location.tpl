%amount=5
%contains=location,organization


dn=%generate_unique_dn(%(base)s,%(l)s)f
l=%sn()f
o=%(l)s
description=%(l)s
objectClass=location
objectClass=organization
