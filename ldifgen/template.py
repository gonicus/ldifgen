class Template(object):

    parameters = None
    lines = None

    def __init__(self, parameter, lines):
        self.lines = lines
        self.parameter = parameter

    def getLines(self):
        return self.lines
