#!/usr/bin/env python
import argparse
import pkg_resources
from ldifgen.generator import Generator


def main():
    p = argparse.ArgumentParser(description="This program generates a ldif containing the given set of objects (user, groups, ...) that can easily imported into your ldap server for demo purpose.")

    p.add_argument('-t', '--templatePath', dest="templatePath", default=pkg_resources.resource_filename('ldifgen', 'templates'))
    p.add_argument('-c', '--number-of-containers', dest="containerAmount", default=100, type=int)
    p.add_argument('-n', '--number-of-leafs', dest="leafAmount", default=1000, type=int)
    p.add_argument('-d', '--tree-depth', dest="treeDepth", default=10, type=int)
    p.add_argument('-b', '--base', dest="base", default="dc=example,dc=net", type=str)
    args = p.parse_args()

    generator = Generator(args.templatePath)
    generator.set("containerAmount", args.containerAmount)
    generator.set("leafAmount", args.leafAmount)
    generator.set("treeDepth", args.treeDepth)
    generator.set("base", args.base)
    generator.generate()

if __name__ == '__main__':
    main()
