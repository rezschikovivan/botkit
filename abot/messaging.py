from abc import ABC, abstractmethod
from typing import List, Any, Dict, Iterable
from utils import classproperty

class MsgerMetods(ABC):
    # операции
    @abstractmethod
    async def answer(self, msg, text:str):"""Отвечает на сообщение пользователя"""
    @abstractmethod
    async def reply(self, msg, text:str):""" """
    @abstractmethod
    async def delete(self, msg):""" """
    @abstractmethod
    async def send_reply_kboard(self, msg, text, url=None):""" """
    @abstractmethod
    async def send_inline_kboard(self, msg, text, callback=None, url=None):""" """

class Actions(MsgerMetods):
    # операции
    @staticmethod
    def get_msg(msg):
        return MsgerFactory.make_msger(msg)
    @staticmethod
    async def answer(msg, text):
        msger: ABCMessager = MsgerFactory.make_msger(msg)
        await msger.answer(msg, text)
    @staticmethod
    async def reply(msg, text):
        msger: ABCMessager = MsgerFactory.make_msger(msg)
        await msger.reply(msg, text)
    @staticmethod
    async def delete(msg):
        msger: ABCMessager = MsgerFactory.make_msger(msg)
        await msger.delete(msg)
    @staticmethod
    async def send_reply_kboard(msg, text, url=None):
        msger: ABCMessager = MsgerFactory.make_msger(msg)
        await msger.send_reply_kboard(msg, text, url)
    @staticmethod
    async def send_inline_kboard(self, msg, text, callback=None, url=None):
        msger: ABCMessager = MsgerFactory.make_msger(msg)
        await msger.send_inline_kboard(msg, text, callback, url)

class ABCMessager(MsgerMetods):
    # свойства
    @classproperty
    @abstractmethod
    def data(cls): """ """
    @classproperty
    @abstractmethod
    def text(cls): """ """
    # типы медиа
    @classproperty
    @abstractmethod
    def document(cls): """ """
    @classproperty
    @abstractmethod
    def audio(cls): """ """
    @classproperty
    @abstractmethod
    def video(cls): """ """
    @classproperty
    @abstractmethod
    def location(cls): """ """
    @classproperty
    @abstractmethod
    def voice(cls): """ """
    @classproperty
    @abstractmethod
    def sticker(cls): """ """
    @classmethod
    @abstractmethod
    def msg_type(cls):"""Возвращает тип, который будет приходить в хэндлеры этой библиотеки"""

class MsgerFactory():
    msges: Dict[str, ABCMessager] = {}

    @classmethod
    def make_msger(cls, msg:Any)->ABCMessager:
        """Возвращает мессаджер соответствующий типу сообщения"""
        return cls.msges[str(type(msg))]

    @classmethod
    def registr_component(cls, msger: ABCMessager|None):
        if msger is None: return
        if not isinstance(msger, ABCMessager): raise TypeError("Принимает в качестве аргумента только подклассы ABCMessage")
        cls.msges[str(msger.msg_type())] = msger

class Button():
    def __init__(self, row:int, column:int, text:str, action:str|Dict):
        self.is_callback = True if isinstance(action, dict) else False
        self.row = row
        self.column = column
        self.text = text
        self.action = action

class Keyboard():

    def __init__(self, frame:List[List[str,str]]):
        """Во frame принимается многомерный список, внутри которого каждый список определяет строку и кол-во эл-ов в ней.
         Внутри 'структурирующих' списков первым указывается название кнопки и затем действие. По умолчанию действие это отправка текста, 
         если будет указанна ссылка, то при нажатии будет осуществлённ переход. Также можно указать callback, он указываетя 2-м эл-ом
          списка как значение словаря под любым ключом. """
        self.buttons:List[Button] = []
        self.row = -1
        self.col = -1
        self.parse(frame)

    def parse(self, iterable:Iterable):
        self.col = -1
        for i in iterable:
            if isinstance(i[0], list):#
                self.row += 1
                self.parse(i)
            elif self.row != -1:# если конечная кнопка
                self.col += 1
                try:
                    self.buttons.append(Button(self.row,self.col, i[0],i[1]))
                except IndexError as err:
                    raise TypeError("Неверно указан формат. В корне списка должны лежать строки, а в строках кнопки, состоящие из 2-х эл-ов: [названия, сообщения]. Сообщением может быть url или, если вам нужен calllback, то словарём из 1-го значения с любым ключом.")
            else: raise TypeError("Неверно указан формат. В корне списка должны лежать строки, а в строках кнопки. Корректный формат ввода например для создания окошка из двух строчек для двух кнопок в вверхней строчке и трех в нижней:  [ [[\"name\",\"data\"],[\"name\",\"data\"]], [[\"name\",\"data\"],[\"name\",\"data\"],[\"name\",\"data\"]] ]")

if __name__ == "__main__":
    k = Keyboard([ [["name"],["name",{"clb":"data"}]] ])
    print()