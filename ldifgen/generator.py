import os
import re
import ldif
import pkg_resources
from datetime import timedelta, datetime
from random import randint, choice, randrange, choice, sample
from ldifgen.line import Line
from ldifgen.template import Template


class NoSuchTemplateException(Exception):
    pass


class NoSuchAttribute(Exception):
    pass


class NoSuchFunction(Exception):
    pass


class FunctionHandler(object):
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

        for item in tmp_params:
            if item == ",":
                param_id += 1
                params[param_id] = []
                continue

            if not param_id in params:
                params[param_id] = []

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

        # Process the parameters list to have a single
        # array containing the parameter as strings.
        params = []
        for para in self.params:

            # Walk through all items of this parameter
            # and combine them to a single string.
            result = []
            for item in para:

                # Combine strings
                if type(item) == str:
                    tmp_res = []
                    for e in result:
                        tmp_res.append(e + item)
                    result = tmp_res
                else:

                    # Process non-string items and then append them to the
                    # existing results
                    tmp = item.process()
                    tmp_res = []
                    for t in tmp:
                        for e in result:
                            tmp_res.append(e + t)
                    result = tmp_res

            params.append("".join(result))

        print "->", params
        return self.generator.runExtension(self.name, *params)


class AttributeHandler(object):
    """
    This class represents a variable replacement of a template
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


class Generator(object):

    _templates = {}
    _templatePath = None
    _config = None
    _extension = {}

    all_items = None
    tree_items = None

    def __init__(self, templatePath):
        self._config = {'containerAmount': 20, 'leafAmount': 100, 'treeDepth': 5, 'base': 'dx=example,dc=net'}
        self._templatePath = templatePath
        self._loadTemplates()
        self._loadExtensions()

    def set(self, name, value):
        self._config[name] = value

    def runExtension(self, name, *params):
        try:
            return self._extension[name].execute(self.current_object, *params)

        except KeyError:
            raise NoSuchFunction("extension %s is not available" % name)

#        except Exception as e:
#            raise TypeError("parameter mismatch for method %s: %s" % (name, str(e)))

    def _loadExtensions(self):
        for entry in pkg_resources.iter_entry_points("ldifgen.extension"):
            mod = entry.load()
            self._extension[entry.name] = mod(self.all_items)

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
                    replacement = AttributeHandler(self, matched[2:-2])

                # Replace item with a function class
                if matched[-1] == "f":
                    replacement = FunctionHandler(self, lineList[start:end])

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

        _container_amount = self._config['containerAmount']
        _leaf_amount = self._config['leafAmount']
        _max_depth = self._config['treeDepth']
        _base = self._config['base']

        # The tree root
        tree = {'item': 'domain', 'children': {}, 'content': {'dn' : [_base]}, 'base': '', 'dn': ''}

        # A list of all items
        allitems = []

        # A list of types to items
        items_by_type = {}

        # Leafs types
        leaf_item_types = []
        leaf_item_amounts = {}

        self.all_items = items_by_type
        self.tree_items = tree


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
            cur_depth = randrange(_max_depth)
            while cur_depth:
                cur_depth -= 1
                if len(item['children'].keys()):
                    item = item['children'][choice(item['children'].keys())]
                else:
                    cur_depth = 0

            clist = getContainerList(item['item'])
            if not clist:
                continue

            # Add the container
            ctype = choice(clist)
            addItem(item, ctype)
            _container_amount -= 1

            # Add forced elements
            if "force_append" in self._templates[ctype].parameter:
                for fitem in self._templates[ctype].parameter['force_append'].split(","):
                    addItem(item, fitem)
                    _container_amount -= 1

        while len(leaf_item_amounts):

            # Randomly get one leaf type
            ctype = choice(leaf_item_amounts.keys())
            leaf_item_amounts[ctype] -= 1
            if leaf_item_amounts[ctype] <=0:
                del(leaf_item_amounts[ctype])

            # Get possible parents
            containers = getParentList(ctype)

            # Randomly choose one parent and add a leaf item
            container = choice(containers)
            addItem(choice(items_by_type[container]), ctype)

        # Method to print the tree
        def print_rec_content(item):
            dn = item['content']['dn'][0]
            print "# " + item['item']
            del(item['content']['dn'])
            print ldif.CreateLDIF(dn, item['content'])
            if len(item['children'].keys()):
                for sitem in item['children']:
                    print_rec_content(item['children'][sitem])

        print_rec_content(tree)

    def create_entry(self, template, base):
        """
        Create a new entry based on the given template
        """

        self.current_object = {'base' : base}

        lines_left = range(0, len(self._templates[template].getLines()))
        results = {}
        last_len = 0
        last_exception = None

        # Walk through each line until all are processed
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
