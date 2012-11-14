%amount=20
%contains=


dn=%generate_unique_dn(%(base)s,cn,%(cn)s)f
cn=%sn()f
gidNumber=%generate_unique_id(gidNumber)f
memberUid=%select_multiple(gosa-user,uid,10)f
objectClass=top
objectClass=posixGroup
