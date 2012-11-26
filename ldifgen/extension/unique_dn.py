from itertools import combinations
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

        dn = "%s=%s,%s" % (attribute, value, base)
        if dn in self._cache:
            av_attrs = filter(lambda x: not x in ['objectClass', 'base', attribute], entry.keys())
            for i in range(0, len(av_attrs)):
                com = combinations(av_attrs, i + 1)
                if com:
                    for c in sorted(com, key=len):
                        ndn = "%s=%s+%s,%s" % (attribute, value, "+".join(["%s=%s" % (rdna, entry[rdna][0]) for rdna in c]), base)
                        if not ndn in self._cache:
                            dn = ndn
                            break

        if dn in self._cache:
            raise NoSuchAttribute()

        self._cache[dn] = None

        return [dn]
