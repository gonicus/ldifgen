# -*- coding: utf-8 -*-
import os
import pkg_resources
from random import randint, choice
from unidecode import unidecode
from ldifgen.extension import IExtension
from ldifgen.generator import NoSuchAttribute


class UniqueIdExtension(IExtension):
    _cache = None

    def __init__(self, generator):
        super(UniqueIdExtension, self).__init__(generator)
        self._cache = {}

    def execute(self, entry, attribute, start=1000):
        if not attribute in self._cache:
            self._cache[attribute] = int(start)

        _id = self._cache[attribute]
        self._cache[attribute] += 1

        return ["%d" %_id]
