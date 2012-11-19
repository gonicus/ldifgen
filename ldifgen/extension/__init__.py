class IExtension(object):

    def __init__(self, all_ref):
        self.all_items = all_ref

    def execute(self, entry):
        raise NotImplementedError("Extension lacks 'exec' method")
