%amount=5
%contains=locality,organization,organizationalUnit


dn=%generate_unique_dn(%(base)s,l,%(l)s)f
l=%sn()f
description=%(l)s
objectClass=locality
