# -*- coding: utf-8 -*-
import os
import pkg_resources
import string
from random import randint, choice
from unidecode import unidecode
from ldifgen.extension import IExtension
from ldifgen.generator import NoSuchAttribute


class UniqueStaticUidExtension(IExtension):

    def __init__(self, generator):
        super(UniqueStaticUidExtension, self).__init__(generator)
        if not 'uid' in self.generator.cache:
            self.generator.cache['uid'] = []

    def execute(self, entry, *args):
        value = None
        while value == None or value in self.generator.cache['uid']:
            value = ''.join([choice(string.letters + string.digits) for i in range(8)])
        self.generator.cache['uid'].append(value)
        return [value]


class UniqueUidExtension(IExtension):

    def __init__(self, generator):
        super(UniqueUidExtension, self).__init__(generator)
        if not 'uid' in self.generator.cache:
            self.generator.cache['uid'] = []

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

        if uid in self.generator.cache['uid']:
            for idx in range(0, 99):
                nuid = "%s%02d" % (uid, idx)
                if not nuid in self.generator.cache['uid']:
                    uid = nuid
                    break

        if uid in self.generator.cache['uid']:
            raise NoSuchAttribute()

        self.generator.cache['uid'].append(uid)

        return [uid]
