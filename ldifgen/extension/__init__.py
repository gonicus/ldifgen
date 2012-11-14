class IExtension(object):

    def __init__(self, generator):
        self.generator = generator

    def execute(self, entry):
        raise NotImplementedError("Extension lacks 'exec' method")
