from abc import ABC , abstractmethod
from typing import List
from abot.mediator import Mediator, purefunc
import inspect

class FilterMethods(ABC):
    """Базовый класс определяющий общьий интерфейс фильтров"""
    @abstractmethod
    def func(self, f:callable): """Фильтр принимающий в качестве параметра функцию и возвращающий объект для обёртывания"""
    @abstractmethod
    def text(self, text):"""Фильтр сравнивающий на полное соответствие текста"""
    @abstractmethod
    def in_text(self, text):"""Фильтр проверяет наличие подстроки в тексте сообщения"""
    @abstractmethod
    def cmnd(self, text):"""Фильтр реагирует на сообщени команды начинающееся с '/'"""
    @abstractmethod
    def photo(self):"""Фильтр реагирует когда присылают сообщение-фото"""
    @abstractmethod
    def video(self):"""Фильтр реагирует когда присылают сообщение-видео"""
    @abstractmethod
    def audio(self):"""Фильтр реагирует когда присылают сообщение-аудио"""
    @abstractmethod
    def document(self):"""Фильтр реагирует когда присылают сообщение-документ"""
    @abstractmethod
    def location(self):"""Фильтр реагирует когда присылают сообщение-локацию"""
    @abstractmethod
    def voice(self):"""Фильтр реагирует когда присылают сообщение-голос"""
    @abstractmethod
    def sticker(self):"""Фильтр реагирует когда присылают стикер"""

class Filter(FilterMethods, Mediator):
    """Класс посредник предоставляет доступ к представлению фильтра. Конкретная реализация (подкласс ABCFilter)
    определяется на этапе регистрации класса-хэндлера в ядре от компонента"""
    __filter_imp:"ABCFilter" = None
    def __init__(self):
        self.filters = []

    def wrapper(self, func):
        #@wraps(func) - сохраняет метаданные о абстратктной приоде функции, поэтоу его тут нельзя использовать, сигнатура подтягивается из родителя
        def wrap(self:Filter, *args):
            f_params = list(inspect.signature(func).parameters.values())[1:]
            if len(args) != len(f_params): raise TypeError("Передано неверное количество аргументов")
            self.filters.append([func.__name__, *args])
            return self
        return wrap

    @property
    def filter_imp(self):return self.__filter_imp
    @filter_imp.setter
    def filter_imp(self, new): self.__filter_imp = new

    @purefunc
    def ivoke_imp(self)-> List[callable] | None:
        """Возвращает фильтры полученные от компонента, используя полиморфную связь через базовый FilterMethods"""
        if self.filter_imp is None: return None
        final_filters = []
        for f in self.filters:
            final_filters.append(self.filter_imp.__getattribute__(f[0])(*f[1:]))
        return final_filters

class ABCFilter(FilterMethods):
    """Методы наследников этого класса должны переопределять методы-фильтры для возвращения фильтрующего обьекта соответствующей библиотеки"""
    @abstractmethod
    def func(self, f):pass
    def text(self, text): return self.func(lambda x : x.text == text)
    def in_text(self, text): return self.func(lambda x : text in x.text)
    def cmnd(self, text): return self.func(lambda x : x.text == f"/{text}")

class Handler():
    '''Декоратор, помечающий ядру, что этот медод является хэндлером. В конструкторе указываются экземпляры Filter'''
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