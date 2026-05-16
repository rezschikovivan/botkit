from  abot.message import MsgFactory
from abot.filter import Filter

class Handler():
    '''Декоратор, помечающий ядру, что этот медод является хэндлером. В конструкторе указываются экземпляры Filter'''
    def __init__(self, *filters:Filter):
        self.filters = filters
        self.func_cls = "хаывдсч"
        self.is_wrapped = False

    def __get__(self, instance, owner):
        print(instance, " ", owner)

    def __call__(self, func_or_msg = None, *args, **kwds):
        if not self.is_wrapped:
            self.func = func_or_msg
            self.is_wrapped = True
            return self
        if func_or_msg is not None: func_or_msg = MsgFactory.make_msg(func_or_msg)
        return self.func(self.func_cls, func_or_msg, *args, **kwds)
    
    @property
    def __code__(self):
        return self.func.__code__
    @property
    def __defaults__(self):
        return self.func.__defaults__
    @property
    def __kwdefaults__(self):
        return self.func.__kwdefaults__