class SingletonType(type):
    def __call__(cls, *args, **kwargs):
        try:
            return cls.__instance
        except AttributeError:
            cls.__instance = super(SingletonType, cls).__call__(
                *args, **kwargs)
            return cls.__instance


class Data(object):
    __metaclass__ = SingletonType

    def __init__(self, controllers=None):
        if controllers is not None:
            self.controllers = controllers
        else:
            self.controllers = dict()
        self.name_map = dict()
        self.reverse_name_map = dict()
        self.name_map_index = 1

    def getNextName(self, node_name, prefix):
        name = "%s%d" % (prefix, self.name_map_index)
        self.name_map[node_name] = name
        self.reverse_name_map[name] = node_name
        self.name_map_index += 1
        return name

    def getBackEndName(self, node_name):
        return self.name_map[node_name]

    def getFrontEndName(self, base_name):
        return self.reverse_name_map[base_name]
