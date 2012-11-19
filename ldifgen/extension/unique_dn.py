from ldifgen.extension import IExtension
from ldifgen.generator import NoSuchAttribute


class UniqueDNExtension(IExtension):
    _cache = None

    def __init__(self, allref):
        super(UniqueDNExtension, self).__init__(allref)
        self._cache = {}

    def execute(self, entry, base, rdn_attribute):
        print "-"*80
        print entry
        print "-"*80
        if not rdn_attribute in entry:
            raise NoSuchAttribute()

        res = "%s=%s,%s" % (rdn_attribute, entry[rdn_attribute][0], base)
        if res in self._cache:
            #TODO: recursively find a not used RDN
            raise NoSuchAttribute()

        self._cache[res] = None

        return [res]
