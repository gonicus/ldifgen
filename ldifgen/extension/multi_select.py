import os
import pkg_resources
from random import sample
from ldifgen.extension import IExtension
from ldifgen.generator import SkipEntry


class MultiSelectExtension(IExtension):

    def execute(self, entry, typ, attribute, no_items):
        if typ in self.generator.all_items:
            entities = [f['content'][attribute][0] for f in self.generator.all_items[typ]]
            r = sample(entities, (len(entities) % int(no_items)) or 1)
            return r

        raise SkipEntry()
