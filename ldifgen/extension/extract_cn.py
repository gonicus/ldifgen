import os
import ldap
import pkg_resources
from ldifgen.extension import IExtension


class ExtractCN(IExtension):

    def execute(self, entry, dn):
        return [ldap.dn.str2dn(dn)[0][0][1]]
