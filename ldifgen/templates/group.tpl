%amount=20
%contains=


dn=%generate_unique_dn(%(base)s,%(cn)s)f
cn=%sn()f
memberUid=%select_multiple(user,uid,10)f
objectClass=top
objectClass=posixGroup
