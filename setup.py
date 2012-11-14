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

    packages = find_packages('.'),
    package_dir={'': '.'},

    include_package_data = True,
    package_data = {
        'ldifgen': ['data/*', 'templates/*'],
    },

    zip_safe = True,

    install_requires = [
        'python_ldap',
        'unidecode'
    ],

    entry_points = """
        [console_scripts]
        ldifgen = ldifgen.main:main

        [ldifgen.extension]
        dob = ldifgen.extension.dob:DOBExtension
        givenName = ldifgen.extension.givenname:GivenNameExtension
        sn = ldifgen.extension.sn:SnExtension
        structName = ldifgen.extension.structname:StructNameExtension
        select_multiple = ldifgen.extension.multi_select:MultiSelectExtension
        generate_unique_dn = ldifgen.extension.unique_dn:UniqueDNExtension
        generate_unique_uid = ldifgen.extension.unique_uid:UniqueUidExtension
        generate_password = ldifgen.extension.password:PasswordExtension
        generate_unique_id = ldifgen.extension.unique_id:UniqueIdExtension
        generate_phone_number = ldifgen.extension.phone:PhoneExtension
        extract_cn = ldifgen.extension.extract_cn:ExtractCN
        add_gosa_acls = ldifgen.extension.gosa:AddGOsaAcls

    """,
)
