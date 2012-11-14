%amount=0.1
%contains=


dn=%generate_unique_dn(%(base)s,sambaDomainName,%(sambaDomainName)s)f
sambaDomainName=%structName()f
sambaAlgorithmicRidBase=1000
objectClass=sambaDomain
sambaNextUserRid=1000
sambaMinPwdLength=5
sambaPwdHistoryLength=0
sambaLogonToChgPwd=0
sambaMaxPwdAge=-1
sambaMinPwdAge=0
sambaLockoutDuration=30
sambaLockoutObservationWindow=30
sambaLockoutThreshold=0
sambaForceLogoff=-1
sambaRefuseMachinePwdChange=0
sambaSID=S-0-8-15

