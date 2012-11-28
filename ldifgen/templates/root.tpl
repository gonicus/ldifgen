%amount=0
%contains=organization,locality,organizationalUnit,domain
%force_append=people_container,group_container,ldap-admin-user


dn=%(base)s
dc=%extract_cn(%(dn)s)f
o=%(dc)s
description=%(dn)s
objectClass=dcObject
objectClass=organization
objectClass=gosaDepartment
