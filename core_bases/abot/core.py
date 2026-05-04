from abot.handle import Filter, ABCFilter, Handler
from typing import List,Dict, Coroutine,Any, Callable, Set, Tuple
from abot.messaging import ABCMessager, MsgerFactory
from abc import ABCMeta, abstractmethod, ABC
import asyncio
    
class ClsComponenter():
    base_clsmthods: List[str] = []
    @classmethod
    def before(cls, mcs, name, bases, attrs): 
        """Вызывается перед регистрацией"""
        pass
    @classmethod
    def registrate_cmpnt(cls ,mcs, name, bases, attrs)-> Tuple["CoreMeta", str, Tuple[object], Dict[str,object]]:
        """ """
        return (mcs, name, bases, attrs)
    @classmethod
    def after(cls, new_cls:"BaseComponent", mcs, name, bases, attrs): 
        """Вызывается после регистрации и проверки имплементации абстрактных методов"""
        MsgerFactory.registr_component(new_cls.get_messager())
        if not isinstance(new_cls.get_messager(), ABCMessager): print(f"Warning! {name}.get_messager() not returns ABCMessager instance. The functionality of sending messages and related features will be unavailable.")
        if not isinstance(new_cls.get_filter(), ABCFilter): print(f"Warning! {name}.get_filter() not returns ABCFilter instance. The functionality of filtering messages and related features will be unavailable.")
class ClsHandler():
    base_cmpnts:Set["BaseComponent"] = set()
    @classmethod
    def before(cls, mcs, name, bases, attrs):
        """Вызывается перед регистрацией класса-хендлера""" 
        pass
    @classmethod
    def registrate_handler(cls, mcs, name:str, bases: Tuple[object], attrs:Dict[str,Any])-> Tuple["CoreMeta", str, Tuple[object], Dict[str,object]]:
        # находим компонент этого класса
        base_cmpnt: BaseComponent
        for b in bases:
            if issubclass(b,BaseComponent):# если b подкласс BaseComponent, то значит все правильно
                base_cmpnt = b
                break
        else: raise BaseException(f"Класс-хэндлер {name} необходимо наследовать от компонента реализующего BaseComponent")# если меткласс указали напрямую 
        o_bases: List[Dict] = list(bases)
        cls.base_cmpnts.add(o_bases[o_bases.index(base_cmpnt)])

        #составляем аттрибуты класса в одном cловаре с родительсими
        all_attrs:Dict = dict()
        for c in o_bases:
            for n, a in c.__dict__.items():
                if not n.startswith("_") or n == "__TOKEN__":
                    all_attrs[n] = a
        
        for n, a in attrs.items():
           if not n.startswith("_") or n == "__TOKEN__":
                all_attrs[n] = a

        # ищем токен
        token = all_attrs.get("__TOKEN__")
        if token is None: raise ValueError(f"Необходимо указать значение переменной класса: __TOKEN__ в {name}")
        base_cmpnt.add_bot(token)

        # добавляет мессанджер компонент в фабрику
        MsgerFactory.registr_component(base_cmpnt.get_messager())

        # регистриуем хэндлеры с фильтрами 
        for k, i in all_attrs.items():
            if isinstance(i, Handler):
                fltrs = []
                for f in i.filters:
                    f.filter_imp = base_cmpnt.get_filter() if isinstance(base_cmpnt.get_filter(), ABCFilter) else None
                    if f.filter_imp is None: break
                    fltrs.extend(f.ivoke_imp())
                #fltrs = fltrs if not fltrs is [] else None
                base_cmpnt.register_method(token, i, *fltrs)

        return (mcs, name, bases, attrs)
    
    @classmethod
    def after(cls, new_cls, mcs, name, bases, attrs):
        """Вызывается после регистрации и проверки на реализации абстрактных методов""" 

    @classmethod
    async def activate_pollings(cls):
        """ Запускает поллинг всех ботов """
        corouts = list()
        for b in cls.base_cmpnts:
            tasks = b.cretae_polling_tasks()
            for task in tasks:
                corouts.append(task)
        return await asyncio.gather(*corouts)


class CoreMeta(ABCMeta):
    __cls_component = ClsComponenter # класс для добваления классов интегрирующих работу с API
    __cls_handler = ClsHandler         # класс для добавления классов-хэндлеров

    def __new__(mcs, name:str, bases, attrs:Dict[str,Any]):
        if name == "BaseComponent":# если это базовый класс
            mcs.__cls_component.base_clsmthods = [ i for i in attrs.keys() if not i.startswith("__") and isinstance(attrs[i], classmethod)]
        else:
            if BaseComponent in bases:
                # Если это класс регистратор
                mcs.__cls_component.before(mcs, name, bases, attrs)
                new_values = mcs.__cls_component.registrate_cmpnt(mcs, name, bases, attrs)
                cls = super().__new__(*new_values)
                cls()
                mcs.__cls_component.after(cls, *new_values)
                return super().__new__(*new_values)
            else:
                # Если это класс-релизация
                mcs.__cls_handler.before(mcs, name, bases, attrs)
                new_values = mcs.__cls_handler.registrate_handler(mcs, name, bases, attrs)
                cls = super().__new__(*new_values)
                cls()
                mcs.__cls_handler.after(cls, *new_values)
                return super().__new__(*new_values)
        return super().__new__(mcs, name, bases, attrs)
    @classmethod
    def set_cls_componenter(cls, new_registrator: ClsComponenter):
        """Заменяет класс для работы с классами-регистраторами внутри ядра"""
        if issubclass(new_registrator, ClsComponenter):
            cls.__cls_component = new_registrator
        else: raise TypeError("Должен быть субкалссом: ClsRegistrator")
    @classmethod
    def set_handlers_registrator(cls, new_registrator: ClsHandler):
        """Заменяет класс для работы с классами-хэндлерами внутри ядра"""
        if issubclass(new_registrator, ClsHandler):
            cls.__cls_handler = new_registrator
        else: raise TypeError("Должен быть субкалссом: ClsHandler")
    @classmethod
    def get_cls_handler(cls)-> ClsHandler:
        """Возвращет текущий класс для работы с классами-хэндлерами внутри ядра"""
        return cls.__cls_handler
    @classmethod
    def get_cls_componenter(cls)-> ClsComponenter:
        """Возвращает текущий класс для работы с классами-регистраторами внутри ядра"""
        return cls.__cls_component

    
def start_bots():
    """Запускает асинхронный цикл соытий для поллинга все добавленых ботов"""
    return CoreMeta.get_cls_handler().activate_pollings()

def set_cmpnts_registrator(new_registrator: ClsComponenter):
    """Заменяет класс для работы с классами-регистраторами внутри ядра"""
    CoreMeta.set_cls_componenter(new_registrator)

def set_handlers_registrator(new_registrator:ClsHandler):
    """Заменяет класс для работы с классами-хэндлерами внутри ядра"""
    CoreMeta.set_handlers_registrator(new_registrator)


# Базовый класс для классов регистраторов
class BaseComponent(metaclass=CoreMeta):
    """ Базовый класс для классов-регистраторов"""
    bots = {}
    
    @classmethod
    @abstractmethod
    def get_filter(cls)-> ABCFilter|None:
        """  """

    @classmethod
    @abstractmethod
    def get_messager(cls)-> ABCMessager|None:
        """  """

    @classmethod
    @abstractmethod
    def add_bot(cls, token:str):
        """ Добавляет экземпляр бота в поле bots, если такого токена еще не было. """

    @classmethod
    @abstractmethod
    def register_method(cls, token, method, *filters):
        """ Регистрирует переданный метод как обработчик в боте под указанным токеном. """

    @classmethod
    @abstractmethod
    def cretae_polling_tasks(cls)->Coroutine:
        """ Возвращает корутину для переодического опроса сервера (поллинга)."""