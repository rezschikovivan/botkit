from abc import ABC, abstractmethod
from typing import List, Any, Dict, Iterable
from abot.mediator import Mediator, purefunc

class MsgerMetods(ABC):
    """Базовый класс определяющий общьий интерфейс мессаджеров"""
    @abstractmethod
    async def answer(msg, text:str):"""Отвечает на сообщение пользователя"""
    @abstractmethod
    async def reply(msg, text:str):""" """
    @abstractmethod
    async def delete(msg):""" """
    @abstractmethod
    async def send_reply_kboard(msg, keyboard:Keyboard, text:str|None = None):""" """
    @abstractmethod
    async def send_inline_kboard(msg, keyboard:Keyboard, text:str|None = None):""" """

class Actions(MsgerMetods, Mediator):
    """Класс-посредник, реализующий отправку сообщений и их чтение"""
    def wrapper(self, func:function):
        @staticmethod
        #@wraps(func) необязательно использовать (даже не рекомендованно из-за возможного сохранения абстрактной природы метода), сигнатура подтягивается из родителя
        async def wrap(msg, *args):
            msger: ABCMsger = MsgerFactory.make_msger(msg)
            await msger.__getattribute__(func.__name__)(msg, *args)
        return wrap
    @purefunc
    @staticmethod
    def get_msg(msg):
        """Возвращает экземпляр ABCMSger для этого сообщения"""
        return MsgerFactory.make_msger(msg)

class ABCMsger(MsgerMetods):
    """Методы наследников этого класса должны переопределять методы для выполнения действия в соответствующей библиотеке"""
    @abstractmethod
    def __init__(self, msg):
        self.msg = msg
    # свойства
    @property
    @abstractmethod
    def date(self):  """Возвращает дату сообщения"""
    @property
    @abstractmethod
    def text(self):  """Возвращает текст сообщения"""
    # типы медиа
    @property
    @abstractmethod
    def photo(self):  """Возвращает фото прикрепленное к этому сообщению"""
    @property
    @abstractmethod
    def document(self):  """Возвращает документ прикрепленный к этому сообщению"""
    @property
    @abstractmethod
    def audio(self): """Возвращает аудио прикрепленное к этому сообщению"""
    @property
    @abstractmethod
    def video(self):  """Возвращает видео прикрепленное к этому сообщению"""
    @property
    @abstractmethod
    def location(self): """ Возвращает локацию"""
    @property
    @abstractmethod
    def voice(self): """Возвращает ГС"""
    @property
    @abstractmethod
    def sender(self)->"Sender":"""Возвращает данные об отправителе"""
    @classmethod
    @abstractmethod
    def msg_type(cls):"""Возвращает тип, который будет приходить в хэндлеры этой библиотеки"""

class MsgerFactory():
    msges: Dict[str, ABCMsger] = {}

    @classmethod
    def make_msger(cls, msg:Any)->ABCMsger:
        """Возвращает мессаджер соответствующий типу сообщения"""
        return cls.msges[str(type(msg))](msg)

    @classmethod
    def registr_component(cls, msger: ABCMsger|None):
        """Регистрирует компонент в фабрике мессаджеров"""
        if msger is None: return
        if not issubclass(msger, ABCMsger): raise TypeError("Принимает в качестве аргумента только подклассы ABCMessage")
        cls.msges[str(msger.msg_type())] = msger

class Sender():
    """Класс отправитель. Хранит информацию"""
    def __init__(self, sender_id, first_name=None, last_name=None, username=None):
        self.id = sender_id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username

class Keyboard():
    """Клавиатура инлайн или реплай. В конструкторе указываются списки с информацией о кнопке. Каждый список - это ряд кнопок. Информация о кнопках - это список название:дата. Пример:  [["b11", "data"], ["b12","data"]], [["b21", "data"], ["b22","data"], ["b23", "data"]] """
    def __init__(self, *frame:List[str,str]):
        """ В конструкторе указываются списки с информацией о кнопке. Каждый список - это ряд кнопок. Информация о кнопках - это список название:дата. Пример:  [["b11", "data"], ["b12","data"]], [["b21", "data"], ["b22","data"], ["b23", "data"]] """
        self.buttons:List[Button] = []
        self.row = -1
        self.col = -1
        self.parse(frame)

    def parse(self, iterable:Iterable):
        """Зполняет поле класса buttons списком экземпляров Button"""
        self.col = -1
        for i in iterable:
            if isinstance(i[0], list):#
                self.row += 1
                self.parse(i)
            elif self.row != -1:# если конечная кнопка
                self.col += 1
                try:
                    self.buttons.append(Button(self.row,self.col, i[0],i[1]))
                except IndexError:
                    raise TypeError("Неверно указан формат. В корне списка должны лежать строки, а в строках кнопки, состоящие из 2-х эл-ов: [названия, сообщения]. Сообщением может быть url или, если вам нужен calllback, то словарём из 1-го значения с любым ключом.")
            else: raise TypeError("Неверно указан формат. В корне списка должны лежать строки, а в строках кнопки. Корректный формат ввода например для создания окошка из двух строчек для двух кнопок в вверхней строчке и трех в нижней:  [ [[\"name\",\"data\"],[\"name\",\"data\"]], [[\"name\",\"data\"],[\"name\",\"data\"],[\"name\",\"data\"]] ]")

class Button():
    """Класс-кнопка. Содержит информацию о строчке, колонке и названии кнопки."""
    def __init__(self, row:int, column:int, text:str, action:str|Dict = None):
        self.is_callback = isinstance(action, dict)
        self.is_url = True if "http" in action and not self.is_callback else False
        self.row = row
        self.column = column
        self.text = text
        self.action = action

if __name__ == "__main__":
    k = Keyboard([["name", "adata"], ["name","data"]] )
    print()