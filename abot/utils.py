
class ClassProperty:
    def __init__(self, prop):
        self.func = prop
    def __get__(self, inst, klass=None):
        if klass is None:
            klass = type(inst)
        return self.func(klass)
def classproperty(func):
    return ClassProperty(func)