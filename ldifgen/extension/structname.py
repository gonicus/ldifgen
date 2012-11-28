import os
import pkg_resources
from random import randint, choice
from ldifgen.extension import IExtension


class StructNameExtension(IExtension):

    def __init__(self, generator):
        super(StructNameExtension, self).__init__(generator)
        data = pkg_resources.resource_filename('ldifgen', 'data')
        self._cache = list(open(os.path.join(data, "structnames.txt")))

    def execute(self, entry):
        return [choice(self._cache).strip()]
