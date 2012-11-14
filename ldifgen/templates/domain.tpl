%amount=0
%contains=organization,locality,organizationalUnit
%force_append=admin-user


dn=%(base)s
dc=%extract_cn(%(dn)s)f
o=%(dc)s
ou=%(dc)s
description=%(dn)s
objectClass=dcObject
objectClass=organization
