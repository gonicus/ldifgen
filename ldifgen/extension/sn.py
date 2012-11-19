import os
import pkg_resources
from random import randint, choice
from ldifgen.extensions import IExtension


class SnExtension(IExtension):
    _cache = None

    def __init__(self, allref):
        super(SnExtension, self).__init__(allref)
        data = pkg_resources.resource_filename('ldifgen', 'data')
        self._cache = list(open(os.path.join(data, "surnames.txt")))

    def exec(self, entry, multi_name_chance=100):
        if randint(0, 100) > multi_name_chance:
            return choice(self._cache).strip() + " " + choice(self._cache).strip()

        return choice(self._cache).strip()
