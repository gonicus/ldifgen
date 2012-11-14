import os
import crypt
import string
import random
from ldifgen.extension import IExtension


class PasswordExtension(IExtension):
    _cache = None

    def __init__(self, generator):
        super(PasswordExtension, self).__init__(generator)

    def execute(self, entry, pwd=None):
        if not pwd:
            pwd = ""
            for i in range(10): #@UnusedVariable
                pwd += random.choice(string.letters + string.digits)

        salt = ""
        for i in range(2): #@UnusedVariable
            salt += random.choice(string.letters + string.digits)

        return ["{crypt}%s" % (crypt.crypt(pwd, salt))]
