%amount=10
%contains=


dn=%generate_unique_dn(%(base)s,uid,%(uid)s)f
objectClass=account
objectClass=posixAccount
objectClass=sambaSamAccount
uidNumber=30012
gidNumber=30001
cn=%generate_unique_uid_static()f
loginShell=/bin/true
gecos=Windows Workstation
uid=%(cn)s$
homeDirectory=/tmp
sambaSID=S-1-5-21-328194278-237061239-1145748033-1019
displayName=FAX
sambaAcctFlags=[W          ]
