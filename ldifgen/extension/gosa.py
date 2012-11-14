import os
import pkg_resources
from random import randint
from datetime import datetime, timedelta
from ldifgen.extension import IExtension


class AddGOsaAcls(IExtension):

    def execute(self, entry, target, subject, kind, action):

        # Try to find the element with the given dn
        for ctype in self.generator.all_items:
            for item in self.generator.all_items[ctype]:
                if target in item['content']['dn']:
                    item['content']['gosaAcl'] = ["Wrust"]

        return [""]
