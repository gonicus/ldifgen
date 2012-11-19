import os
import pkg_resources
from random import randint, choice
from ldifgen.extensions import IExtension


class UniqueUidExtension(IExtension):
    _cache = None

    def __init__(self, allref):
        super(UniqueUidExtension, self).__init__(allref)
        self._cache = {}

    def exec(self, entry, *args):
        uid = ''.join(args).lower()[0:8]
        uid = uid.lower()
        return [uid]
