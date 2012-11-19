from ldifgen.extensions import IExtension
from ldifgen.generator import NoSuchAttribute


class UniqueDNExtension(IExtension):
    _cache = None

    def __init__(self, allref):
        super(UniqueDNExtension, self).__init__(allref)
        self._cache = {}

    def exec(self, entry, rdn_attribute, base, value):
        res = ["%s=%s,%s" % (rdn_attribute, value, base)]
        if res in self._cache:
            #TODO: recursively find a not used RDN
            raise NoSuchAttribute()

        self._cache[res] = None

        return res
