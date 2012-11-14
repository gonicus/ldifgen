%amount=5
%contains=


dn=%generate_unique_dn(%(base)s,cn,%(cn)s)f
cn=%structName()f
member=%select_multiple(gosa-user,dn,10)f
member=%select_multiple(group,dn,10)f
gosaGroupObjects=[UG]
objectClass=top
objectClass=gosaGroupOfNames
