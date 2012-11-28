%amount=2
%contains=organization,locality,organizationalUnit
%force_append=people_container,group_container,ldap-admin-user

dn=%generate_unique_dn(%(base)s,dc,%(dc)s)f
dc=%structName()f
o=%(dc)s
description=%(dn)s
objectClass=dcObject
objectClass=locality
objectClass=gosaDepartment
