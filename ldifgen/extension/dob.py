import os
import pkg_resources
from random import randint
from datetime import datetime, timedelta
from ldifgen.extension import IExtension


class DOBExtension(IExtension):

    def execute(self, entry, _from=18, _to=99):
        start = datetime.now() - timedelta(days=365 * _to)
        end = datetime.now() - timedelta(days=365 * _from)
        return [(start + timedelta(seconds=randint(0, int((end - start).total_seconds())))).strftime("%Y-%m-%d")]
