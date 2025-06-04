class EnvFrame:
    def __init__(self, parent=None):
        self.vars = {}
        self.parent = parent

    def lookup(self, name):
        if name in self.vars:
            return self.vars[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Variable '{name}' non définie.")

    def insert(self, name, value):
        self.vars[name] = value

    def copy_shallow(self):
        """
        Retourne une copie dont les variables sont copiées, mais pas le parent.
        """
        newf = EnvFrame(self.parent)
        newf.vars = self.vars.copy()
        return newf