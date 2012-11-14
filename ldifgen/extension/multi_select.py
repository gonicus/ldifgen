import os
import pkg_resources
from random import sample
from ldifgen.extension import IExtension


class MultiSelectExtension(IExtension):

    def execute(self, entry, typ, attribute, no_items):
        if typ in self.generator.all_items:
            entities = [f['content'][attribute][0] for f in self.generator.all_items[typ]]
            return sample(entities, len(entities) % int(no_items))

        return []
