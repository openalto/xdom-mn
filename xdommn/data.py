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
