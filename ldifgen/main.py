#!/usr/bin/env python
import argparse
import os
import re
import random
import sys
from datetime import timedelta, datetime
from random import randint, choice




class NoSuchTemplateException(Exception):
    pass


class NoSuchAttribute(Exception):
    pass


class NoSuchFunction(Exception):
    pass


class Template(object):

    parameters = None
    lines = None

    def __init__(self, parameter, lines):
        self.lines = lines
        self.parameter = parameter

    def getLines(self):
        return self.lines


class Line(object):
    """
    This class is used in the template parser to represent an
    attribute of an template.

    This class generates the output for a single attriubte of a template.
    Replacements like %(variable)s or %function)f will be replaced by the
    expected content.
    """

    generator = None
    attrName = None
    elements = None
    id = None
    next_id = 0

    def __init__(self, generator, attrName, elements):
        self.generator = generator
        self.attrName = attrName
        self.elements = elements
        self.id = Line.next_id
        Line.next_id += 1

    def __repr__(self):
        return self.attrName + ": ..."

    def process(self):
        """
        Process the contents of this line element
        and return a computet value it.

        All function calls and variables will be replaced.
        """

        result = ['']
        for item in self.elements:
            if type(item) == str:
                tmp_res = []
                for e in result:
                    tmp_res.append(e + item)
                result = tmp_res
            else:
                tmp = item.process()
                tmp_res = []
                for t in tmp:
                    for e in result:
                        tmp_res.append(e + t)
                result = tmp_res

        # Tell the generator about the newly created attribute
        self.generator.current_object[self.attrName] = result
        return self.attrName, result


class getFunction(object):
    """
    This class is used during the template parsing to replace
    function calls defined in the template with real functions.
    """

    name = None
    generator= None
    params = None

    def __init__(self, generator, parts):

        # Extract the functions name and the parameter list
        name = re.sub("^([^(]*).*$", "\\1", "".join([f for f in parts[1:-1] if type(f) in [str]]))
        tmp_params = parts[len(name)+2:-2]

        # Prepare parameter list. Separate parameter list into single parameters.
        params = {}
        param_id = 0
        params[param_id] = []
        for item in tmp_params:
            if item == ",":
                param_id = param_id + 1
                params[param_id] = []
                continue

            params[param_id].append(item)

        # Store values to be able access them during process
        self.params = params.values()
        self.name = name
        self.generator = generator

    def __repr__(self):
        return self.name + "(...)"

    def process(self):
        """
        Executes the function and returns the result

        Parameters will be processed before if necessary.
        """
        try:
            func = getattr(self.generator, self.name)
        except:
            raise NoSuchFunction("no such function %s!" % (self.name))

        params = []
        for para in self.params:
            result = ['']
            for item in para:
                if type(item) == str:
                    tmp_res = []
                    for e in result:
                        tmp_res.append(e + item)
                    result = tmp_res
                else:
                    tmp = item.process()
                    tmp_res = []
                    for t in tmp:
                        for e in result:
                            tmp_res.append(e + t)
                    result = tmp_res
            params.append("".join(result))

        res = func(params)
        return res


class getAttr(object):
    """
    This class represents a variable replacement of a tempalte
    e.g. %(variableName)s

    When this class is processed, it returns the content of the
    variable.
    """

    name = None
    generator= None

    def __init__(self, generator, name):
        self.name = name
        self.generator = generator

    def __repr__(self):
        return "<"+self.name+">"

    def process(self):
        if not self.name in self.generator.current_object:
            raise NoSuchAttribute("unknown attribute %s" % (self.name))
        return self.generator.current_object[self.name]


class LdifGenerator(object):

    _use = {}
    _templates = {}
    _templatePath = None

    def __init__(self, templatePath):
        self._templatePath = templatePath
        self._loadTemplates();

    def generate_unique_dn(self, args):
        res = ["cn=%s,%s" % (args[1], args[0])]
        return res

    def generate_unique_uid(self, args):
        uid = ''.join(args).lower()[0:8]
        return [uid]

    def dob(self, args):
        """
        Generate date of birth for people between 18 and 99
        """
        start = datetime.now() - timedelta(days=365*100)
        end = datetime.now() - timedelta(days=365*18)
        return [(start + timedelta(seconds=randint(0, int((end - start).total_seconds())))).strftime("%Y-%m-%d")]

    def select_multiple(self, args):
        return( ["a", "b"])

    def givenName(self, args):
        if bool(randint(0, 1)):
            return [self._name_gen('data/givennames-f.txt', 85)]

        return [self._name_gen('data/givennames-m.txt', 85)]


    def sn(self, args):
        return [self._name_gen('data/surnames.txt', 90).strip()]


    def _name_gen(self, lst, multi_name_chance=100):
        lst = list(open(lst))

        if randint(0, 100) > multi_name_chance:
            return choice(lst).strip() + " " + choice(lst).strip()

        return choice(lst).strip()

    def use(self, o_type, amount):
        """
        Tell the generator to use the given type of object while generating
        the ldif.
        """
        if o_type not in self._templates:
            raise NoSuchTemplateException("missing template for '%s'!" % (o_type))
        self._use[o_type] = amount

    def _loadTemplates(self):
        """
        Loads all templates, from the given tempalte path.
        The templates will be stored in self._templates.
        """
        fileList = []
        for root, subFolders, files in os.walk(self._templatePath):
            for file in files:
                path = os.path.join(root, file)
                self._templates[os.path.splitext(file)[0]] = self._processTemplate(open(path).read());

    def _processTemplate(self, content):
        """
        Parses the template into a some-kind of a process list.
        This process-list will then be executed in the generate method
        to produce ldif entries.
        """

        # Parse each line of the template and try to find
        # commands like %function()f or %(variable)s
        lines = content.split("\n")
        objectList = []
        regex = "(^.*(%([a-zA-Z_][a-zA-Z0-9_-]*)?\([^\)\(]*\)[fs]).*)$"
        parameters = {}
        for line in lines:

            # Extract configuration parameters
            if re.match("^[\w]*%", line):
                line = re.sub("^[\w]*\%(.*)", "\\1", line)
                items = line.split("=")
                parameters[items[0].strip()] = items[1].strip()
                continue

            # Extract the attribute name and the line defintiion
            attrName = re.sub("^([^=]*)=.*$", "\\1" , line)
            line = re.sub("^[^=]*=(.*)$", "\\1" , line)
            match = re.match(regex, line)
            lineList = list(line)

            # While there is still a function call or a variable defintion
            # in the line, extract it.
            while match:
                line = match.group(0)
                matched = match.group(2)
                start = match.start(2)
                end = match.end(2)

                # Replace item with a variable class
                if matched[-1] == "s":
                    replacement = getAttr(self, matched[2:-2])

                # Replace item with a function class
                if matched[-1] == "f":
                    replacement = getFunction(self, lineList[start:end])

                # Replace function/variable with its replacement
                line = line[0:start] + "!" +line[end:]
                lineList = lineList[0:start] + [replacement] + lineList[end:]
                match = re.match(regex, line)

            # Collect all parsed line elements
            if attrName:
                line_object = Line(self, attrName, lineList)
                objectList.append(line_object)

        if not "contains" in parameters:
            raise Exception("missing template parameter: %s" % ("contains"))
        if not "amount" in parameters:
            raise Exception("missing template parameter: %s" % ("amount"))

        # Prepare the contains parameter
        clist = []
        if parameters['contains']:
            contains = parameters['contains'].split(",")
            for item in contains:
                clist.append(item.strip())
        parameters['contains'] = clist
        parameters['amount'] = int(parameters['amount'])

        return Template(parameters, objectList)


    def generate(self):
        """
        Generate the ldif output.
        """

        _container_amount = 200
        _leaf_amount = 1000
        _max_depth = 10;
        _base = "dc=gonicus,dc=de"

        # The tree root
        tree = {'item': 'domain', 'children': {}, 'content': {'dn' : [_base]}, 'base': '', 'dn': ''}

        # A list of all items
        allitems = []

        # A list of types to items
        items_by_type = {}

        # Leafs types
        leaf_item_types = []
        leaf_item_amounts = {}

        # Calculate amount of leaf elements
        _leaf_amount_frac = 0
        for template in self._templates:
            if not(len(self._templates[template].parameter['contains'])):
                _leaf_amount_frac += self._templates[template].parameter['amount']
                leaf_item_types.append(template)
        for template in leaf_item_types:
            leaf_item_amounts[template] = _leaf_amount * self._templates[template].parameter['amount'] / _leaf_amount_frac

        # Build list of container elements
        def getContainerList(ctype):
            contains = self._templates[ctype].parameter['contains']
            containerList = []
            for item in contains:
                if not item in self._templates:
                    raise NoSuchTemplateException("no such template %s" % (item))
                if not self._templates[item].parameter['contains']:
                    continue
                for i in range(int(self._templates[item].parameter['amount'])):
                    containerList.append(item)
            return containerList

        # Detect possible parents for the given template type
        parent_cache = {}
        def getParentList(ctype):
            if ctype not in parent_cache:
                parent_cache[ctype] = [t for t in self._templates if ctype in self._templates[t].parameter['contains']]
            return parent_cache[ctype]

        # Method to add a new item
        def addItem(item, ctype):
            newitem = {'item': ctype,
                       'children': {},
                       'base': item['content']['dn'],
                       'content': self.create_entry(ctype, item['content']['dn'])}
            allitems.append(newitem)
            if not ctype in items_by_type:
                items_by_type[ctype] = []
            items_by_type[ctype].append(newitem)
            item['children'][len(item['children'].keys())] = newitem

        # Create container tree.
        while _container_amount > 0:
            item = tree
            cur_depth = random.randrange(_max_depth)
            while cur_depth:
                cur_depth -= 1
                if len(item['children'].keys()):
                    item = item['children'][random.choice(item['children'].keys())]
                else:
                    cur_depth = 0

            clist = getContainerList(item['item'])
            if not clist:
                continue

            # Add the container
            ctype = random.choice(clist)
            addItem(item, ctype)
            _container_amount -= 1

            # Add forced elements
            if "force_append" in self._templates[ctype].parameter:
                for fitem in self._templates[ctype].parameter['force_append'].split(","):
                    addItem(item, fitem)
                    _container_amount -= 1

        # Insert leaf elements
        for template in leaf_item_types:
            containers = getParentList(template)
            for i in range(leaf_item_amounts[template]):
                for container in containers:
                    addItem(random.choice(items_by_type[container]), template)

        # Method to print the tree
        def print_rec(item, depth=0):
            print depth * " --> " + item['item']
            if len(item['children'].keys()):
                for sitem in item['children']:
                    print_rec(item['children'][sitem], depth + 1)

        # Method to print the tree
        def print_rec_content(item):
            print "\n\n##" + item['item']
            for k in item['content']:
                print "%s: %s" % (k, item['content'][k])
            if len(item['children'].keys()):
                for sitem in item['children']:
                    print_rec_content(item['children'][sitem])

        print_rec_content(tree)


    def create_entry(self, template, base):

        self.current_object = {'base' : base}

        lines_left = range(0, len(self._templates[template].getLines()))
        results = {}
        last_len = 0
        last_exception = None
        while len(lines_left) and last_len != len(lines_left):
            last_len = len(lines_left)
            for i in range(0, last_len):
                lineid = lines_left.pop(0)
                line = self._templates[template].getLines()[lineid]
                try:
                    attrName, result = line.process()
                    results[line.id] = result
                except NoSuchAttribute as e:
                    #print str(e)
                    last_exception = e
                    lines_left.append(lineid)

        # There are still lines left ... break
        if lines_left:
            unresolveable_attributes = []
            for lineid in lines_left:
                unresolveable_attributes.append(self._templates[template].getLines()[lineid].attrName)
            raise Exception("unresolveable attributes: %s" % (", ".join(unresolveable_attributes)))

        result = {}
        for line in self._templates[template].getLines():
            result[line.attrName] = results[line.id]
        return result

def main():
    p = argparse.ArgumentParser(description="This program generates a ldif containing the given set of objects (user, groups, ...) that can easily imported into your ldap server for demo purpose.")

    p.add_argument('-t', '--templatePath', dest="templatePath", default="templates")
    p.add_argument('-u', '--user', dest="useUsers", default=False, action='store_true')
    p.add_argument('-g', '--groups', dest="useGroups", default=False, action='store_true')
    p.add_argument('-U', '--number-users', dest="numberUsers", default=100, type=int)
    p.add_argument('-G', '--number-groups', dest="numberGroups", default=100, type=int)
    args = p.parse_args()

    generator = LdifGenerator(args.templatePath)
    if args.useUsers:
        generator.use("user", args.numberUsers)

    if args.useGroups:
        generator.use("group", args.numberGroups)

    generator.generate()

if __name__ == '__main__':
    main()
