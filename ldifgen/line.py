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
