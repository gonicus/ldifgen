class IExtension(object):

    def __init__(self, all_ref):
        self.all_items = all_ref

    def exec(entry):
        raise NotImplementedError("Extension lacks 'exec' method")
