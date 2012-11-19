#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "ldifgen",
    version = "0.1",
    author = "GONICUS GmbH",
    author_email = "info@gonicus.de",
    description = "Generation tool for LDAP contents",
    keywords = "system config management ldap groupware",
    license = "LGPL",
    url = "http://www.gonicus.de",
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Systems Administration',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
        'Topic :: System :: Software Distribution',
        'Topic :: System :: Monitoring',
    ],

    packages = find_packages('ldifgen'),
    package_dir={'': 'ldifgen'},

    include_package_data = True,
    package_data = {
        'ldifgen': ['data/*', 'templates/*'],
    },

    zip_safe = True,

    install_requires = [
        'ldap'
    ]

    entry_points = """
        [ldifgen.methods]

        [console_scripts]
        ldifgen = ldifgen.main:main
    """,
)
