import random
import string

class InstanceProperty:
    def __init__(self, prop):
        self.func = prop
    def __get__(self, inst=None, klass=None):
        if klass is None:
            klass = type(inst)
        return self.func(klass)
def instanceproperty(func):
    return InstanceProperty(func)

def random_string(length:int):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



class StaticProperty:
    def __init__(self, prop):
        self.func = prop
    def __get__(self, inst=None, klass=None):
        return self.func()
def staticproperty(func):
    return StaticProperty(func)