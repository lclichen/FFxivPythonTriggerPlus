class AttributeExistsException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Attribute '%s' already exists" % self.name


class AttributeNotFoundException(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return "Attribute '%s' not found" % self.name


class AttrContainer(object):
    def __init__(self, ):
        self.names = set()

    def register_attribute(self, name, obj):
        if hasattr(self, name):
            raise AttributeExistsException(name)
        self.names.add(name)
        setattr(self, name, obj)

    def unregister_attribute(self, name):
        if name not in self.names:
            raise AttributeNotFoundException(name)
        self.names.remove(name)
        delattr(self, name)

    def __getitem__(self, item):
        return getattr(self, item)
