import os
import pkg_resources
from random import sample
from ldifgen.extension import IExtension


class MultiSelectExtension(IExtension):

    def execute(self, typ, attribute):
        if typ in self.all_items:
            entities = [f['content'][attribute][0] for f in self.all_items[typ]]
            return sample(entities, len(entities) % 10)

        return []
