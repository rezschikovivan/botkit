from abc import ABC, abstractmethod
from typing import List, Any
from abot.utils import classproperty

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
    msges: List[ABCMessager] = []

    @classmethod
    def make_msger(cls, msg:Any)->ABCMessager:
        """Возвращает мессаджер соответствующий типу сообщения"""
        for m in cls.msges:
            if isinstance(msg, m.msg_type()):
                return m
        raise TypeError(f"Не зарегестрировано компонента с типом сообщений {type(msg)}")

    @classmethod
    def registr_component(cls, msger: ABCMessager|None):
        if msger is None: return
        if not isinstance(msger, ABCMessager): raise TypeError("Принимает в качестве аргумента только подклассы ABCMessage")
        cls.msges.append(msger)