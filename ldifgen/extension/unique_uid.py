import os
import pkg_resources
from random import randint, choice
from ldifgen.extension import IExtension


class UniqueUidExtension(IExtension):
    _cache = None

    def __init__(self, generator):
        super(UniqueUidExtension, self).__init__(generator)
        self._cache = {}

    def execute(self, entry, *args):
        uid = ''.join(args).lower()[0:8]
        uid = uid.lower()
        return [uid]
