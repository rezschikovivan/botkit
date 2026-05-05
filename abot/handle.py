from abc import ABC , abstractmethod
from typing import List, Dict, Any, Callable
from abot.utils import staticproperty
import inspect

class FilterMethods(ABC):
    @abstractmethod
    def func(self, f:callable): """Фильтр принимающий в качестве параметра функцию и возвращающий объект для обёртывания"""
    @abstractmethod
    def text(self, text):"""Фильтр сравнивающий на полное соответствие текста"""
    @abstractmethod
    def in_text(self, text):"""Фильтр проверяет наличие подстроки в тексте сообщения"""
    @abstractmethod
    def cmnd(self, text):"""Фильтр реагирует на сообщени команды начинающееся с '/'"""
    @staticproperty
    @abstractmethod
    def photo(self):"""Фильтр реагирует когда присылают сообщение-фото"""
    @staticproperty
    @abstractmethod
    def video(self):""" """
    @staticproperty
    @abstractmethod
    def audio(self):""" """
    @staticproperty
    @abstractmethod
    def document(self):""" """
    @staticproperty
    @abstractmethod
    def location(self):""" """
    @staticproperty
    @abstractmethod
    def voice(self):""" """
    @staticproperty
    @abstractmethod
    def sticker(self):""" """

class Filter(FilterMethods):
    """Класс предоставляет доступ к абстрактному представлению понятия фильтра. Конкретная реализация (подкласс Implementor)
    определяется в ходе выполнения (на основе класса-регистратора реализующего фабричный метод)"""
    __filter_imp:"ABCFilter" = None

    def __init__(self, *args):
        self.filters = []
        
    @property
    def filter_imp(self):return self.__filter_imp
    @filter_imp.setter
    def filter_imp(self, new): self.__filter_imp = new
    def ivoke_imp(self)-> List[callable] | None:
        if self.filter_imp is None: return None
        final_filters = []
        for f in self.filters:
            final_filters.append(self.filter_imp.__getattribute__(f[0])(*f[1:]))
        return final_filters
    def func(self, f):
        self.filters.append([self.func.__name__, f])
        return self
    def text(self, text)->"Filter": 
        self.filters.append([self.text.__name__, text])
        return self
    def in_text(self, text)-> "Filter":
        self.filters.append([self.in_text.__name__, text])
        return self
    def cmnd(self, text) -> "Filter" :
        self.filters.append([self.cmnd.__name__, text])
        return self
    @staticproperty
    def photo(self) -> "Filter" :
        self.filters.append([self.photo.__name__])
        return self
    @staticproperty
    def video(self):
        self.filters.append([self.video.__name__])
        return self
    @staticproperty
    def audio(self):
        self.filters.append([self.audio.__name__])
        return self
    @staticproperty
    def document(self):
        self.filters.append([self.document.__name__])
        return self
    @staticproperty
    def location(self):
        self.filters.append([self.location.__name__])
        return self
    @staticproperty
    def voice(self):
        self.filters.append([self.voice.__name__])
        return self
    @staticproperty
    def sticker(self):
        self.filters.append([self.sticker.__name__])
        return self
    
class ABCFilter(FilterMethods):
    """Методы наследников этого класса должны переопределять методы-фильтры для возвращения фильтрующего обьекта соответствующей библиотеки"""
    @abstractmethod
    def func(self, f):pass
    def text(self, text): return self.func(lambda x : x.text == text)
    def in_text(self, text): return self.func(lambda x : text in x.text)
    def cmnd(self, text): return self.func(lambda x : x.text == f"/{text}")

class Handler():
    '''Декоратор, помечающий ядру, что этот медод является хэндлером. В конструкторе указываются фильтры'''
    def __init__(self, *filters:Filter):
        self.filters = filters
        self.is_set = False

    def __call__(self, func = None, *args, **kwds):
        if not self.is_set:
            self.func = func
            self.is_set = True
            return self
        return self.func(func, *args, **kwds)
    
    @property
    def __code__(self):
        return self.func.__code__
    @property
    def __defaults__(self):
        return self.func.__defaults__
    @property
    def __kwdefaults__(self):
        return self.func.__kwdefaults__