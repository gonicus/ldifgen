from ldifgen.extension import IExtension
from ldifgen.generator import NoSuchAttribute


class UniqueDNExtension(IExtension):
    _cache = None

    def __init__(self, generator):
        super(UniqueDNExtension, self).__init__(generator)
        self._cache = {}

    def execute(self, entry, base, attribute, value):
        if not attribute in entry:
            raise NoSuchAttribute()

        res = "%s=%s,%s" % (attribute, value, base)
        if res in self._cache:
            #TODO: recursively find a not used RDN
            raise NoSuchAttribute()

        self._cache[res] = None

        return [res]
