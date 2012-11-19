import os
import pkg_resources
from random import randint, choice
from ldifgen.extensions import IExtension


class GivenNameExtension(IExtension):
    _cache_m = None
    _cache_f = None

    def __init__(self, allref):
        super(GivenNameExtension, self).__init__(allref)

        data = pkg_resources.resource_filename('ldifgen', 'data')
        self._cache_m = list(open(os.path.join(data, "givennames-m.txt")))
        self._cache_f = list(open(os.path.join(data, "givennames-f.txt")))

    def exec(self, entry, multi_name_chance=100, gender=None):
        if not gender:
            gender = bool(randint(0, 1)

        return [self._name_gen(self._cache_m if gender else self._cache_f, multi_name_chance)]

    def _name_gen(self, cache, multi_name_chance):
        if randint(0, 100) > multi_name_chance:
            return choice(cache).strip() + " " + choice(cache).strip()

        return choice(cache).strip()
