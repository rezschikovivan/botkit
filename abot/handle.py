from  abot.message import MsgFactory
from abot.filter import Filter

class Handler():
    '''Декоратор, помечающий ядру, что этот медод является хэндлером. В конструкторе указываются экземпляры Filter'''
    def __init__(self, *filters:Filter):
        self.filters = filters
        self.is_wrapped = False

    def __call__(self, func_or_args = None, *args, **kwds):
        if not self.is_wrapped:
            self.func = func_or_args
            self.is_wrapped = True
            return self
        if func_or_args is not None: func_or_args = MsgFactory.make_msg(func_or_args)
        return self.func(func_or_args, *args, **kwds)
    
    @property
    def __code__(self):
        return self.func.__code__
    @property
    def __defaults__(self):
        return self.func.__defaults__
    @property
    def __kwdefaults__(self):
        return self.func.__kwdefaults__