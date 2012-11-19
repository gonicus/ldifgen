#!/usr/bin/env python
import argparse
import pkg_resources
from ldifgen.generator import Generator


def main():
    p = argparse.ArgumentParser(description="This program generates a ldif containing the given set of objects (user, groups, ...) that can easily imported into your ldap server for demo purpose.")

    p.add_argument('-t', '--templatePath', dest="templatePath", default=pkg_resources.resource_filename('ldifgen', 'templates'))
    p.add_argument('-u', '--user', dest="useUsers", default=False, action='store_true')
    p.add_argument('-g', '--groups', dest="useGroups", default=False, action='store_true')
    p.add_argument('-U', '--number-users', dest="numberUsers", default=100, type=int)
    p.add_argument('-G', '--number-groups', dest="numberGroups", default=100, type=int)
    args = p.parse_args()

    generator = Generator(args.templatePath)
    if args.useUsers:
        generator.use("user", args.numberUsers)

    if args.useGroups:
        generator.use("group", args.numberGroups)

    generator.generate()

if __name__ == '__main__':
    main()
