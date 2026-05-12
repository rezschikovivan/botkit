from abc import ABC, abstractmethod, ABCMeta
from typing import Tuple, Dict, Any, Callable, Iterable, List, overload
from functools import wraps

class MetaMediator(ABCMeta):
    """Класс 'посредник' переопределяет все методы класса на wrapper, что позволяет автоматически имлементировать множество методов с одинаковой реализацие. 
    Методы помеченный декоратором purefunc не будут заменены"""
    def __new__(cls, name:str, bases: Tuple[object], attrs:Dict[str,Any]):
        if name == "Mediator": return super().__new__(cls, name, bases, attrs)
        wrap = attrs.get("wrapper")
        for k, v in attrs.items():
            if not k.startswith("_") and callable(v) and k !="wrapper" and v.__dict__.get("__ispure__") is None:
                attrs[k] = wrap(None, v)
        attrs.update(cls.__find_and_realize_abstractmethods(bases, wrap))
        return super().__new__(cls, name, bases, attrs)
    @abstractmethod
    def wrapper(self, func:Callable):
        """ Возвращает обертку для всех методов класса, которая может в своем теле использовать self. Методы помеченный декоратором purefunc не будут заменены"""
        raise NotImplementedError("Нужно реализовать абстрактный метод wrapper в подклассах Mediator")
    @classmethod
    def __find_and_realize_abstractmethods(cls, bases:Iterable[ABC], realization:Callable)->Dict[str,Callable]:
        """Находит в родителях абстрактные методы и реализует их"""
        return cls.__realize_abstractmethods(cls.__find_abstractmethods_in_bases(bases), realization)
    
    @classmethod
    def __realize_abstractmethods(cls, methods:dict[str, Any], wrap:Callable)->Dict[str,Callable]:
        """Реализует абстрактные (переданные) методы """
        implemention = {}
        for k,v in methods.items():
            implemention[k] = wrap(None, v)
        return implemention

    @classmethod
    def __find_abstractmethods_in_bases(cls, bases:Iterable[object])->Dict[str, Callable]:
        """Находит в родителях абстрактные"""
        methods_to_implement:Dict[str, function] = {}
        for b in bases:
            if type(b) == ABCMeta:
                for m in b.__abstractmethods__:
                        methods_to_implement[m] = b.__dict__.get(m)
        return methods_to_implement
    

class Mediator(metaclass=MetaMediator):
    """Вспомогательный класс, который предоставляет стандартный способ создания посредника с использованием
    наследования.
    """

def purefunc(func):
    """Декоратор помечающий метаклассу MetaMediator, что не нужно заменять этот метод"""
    @wraps(func)
    def wrap(*args, **kwargs):
        return func(*args, **kwargs)
    setattr(wrap, "__ispure__", True)
    return wrap


