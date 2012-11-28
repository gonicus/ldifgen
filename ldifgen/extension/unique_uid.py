# -*- coding: utf-8 -*-
import os
import pkg_resources
from random import randint, choice
from unidecode import unidecode
from ldifgen.extension import IExtension
from ldifgen.generator import NoSuchAttribute


class UniqueUidExtension(IExtension):
    _cache = None

    def __init__(self, generator):
        super(UniqueUidExtension, self).__init__(generator)
        self._cache = {}

    def execute(self, entry, *args):
        mapping = {}
        fmt = "{sn[0]:.7}{givenName[0]:.1}"

        for arg in args:
            if not arg in entry:
                raise NoSuchAttribute()

            mapping[arg] = [e.lower() for e in entry[arg]]

        try:
            uid = fmt.format(**mapping)
            uid = unidecode(uid.decode("utf-8"))
        except UnicodeDecodeError:
            try:
                fmt = "{sn[0]:.8}{givenName[0]:.1}"
                uid = fmt.format(**mapping)
                uid = unidecode(uid.decode("utf-8"))
            except UnicodeDecodeError:
                fmt = "{sn[0]:.7}{givenName[0]:.2}"
                uid = fmt.format(**mapping)
                uid = unidecode(uid.decode("utf-8"))

        if uid in self._cache:
            for idx in range(0, 99):
                nuid = "%s%02d" % (uid, idx)
                if not nuid in self._cache:
                    uid = nuid
                    break

        if uid in self._cache:
            raise NoSuchAttribute()

        self._cache[uid] = None

        return [uid]
