import os
import pkg_resources
from base64 import b64encode
from random import randint
from ldifgen.extension import IExtension


class AddGOsaAcls(IExtension):

    def execute(self, entry, target, subject, kind, action):

        # Try to find the element with the given dn
        target_item = None
        for ctype in self.generator.all_items:
            for item in self.generator.all_items[ctype]:
                if target in item['content']['dn']:
                    target_item = item
                    break

        if not target_item:
            raise Execption("failed to add GOsa acls to %s no such item" % (target))

        if not "gosaAclEntry" in target_item['content']:
            target_item['content']['gosaAclEntry'] = []

        if not "gosaAcl" in target_item['content']['objectClass']:
            target_item['content']['objectClass'].append("gosaAcl")

        aclEntry = str(len(target_item['content']['gosaAclEntry'])) + ":" + kind + ":"
        aclEntry += b64encode(subject) + ":"
        aclEntry += action
        target_item['content']['gosaAclEntry'].append(aclEntry)

        return [""]
