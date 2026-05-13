from abot.core import BaseComponent, BaseFilterImplementor, BaseMsg
from typing import Dict
from aiogram.types import Message
from aiogram.filters import BaseFilter 
from aiogram import Bot, Dispatcher

class CustomFilter(BaseFilterImplementor):
    def __init__(self, *func: callable):
        self.func = func

    def __call__(self, event)->bool:
        for f in self.func:
            if f(event): continue
            return False
        else: return True

class AiogramFilter(BaseFilterImplementor):
    def func(self, f):
        return CustomFilter(f)
    
class AiogramMsger(BaseMsg):
    @classmethod
    def msg_type(cls):
        return Message
    async def answer(msg:Message, text):
        return await msg.answer(text)

# Класс-регистратор в aiogram
class AiogramComponent(BaseComponent):
    bots: Dict[str,Bot] = {}
    dispatchers: Dict[str,Dispatcher] = {}
    @classmethod
    def get_filter(cls):
        pass
    @classmethod
    def get_messager(cls):
        pass
    @classmethod
    def add_bot(cls, token:str):
        if not token in cls.bots.keys():
            cls.bots[token] = Bot(token=token)
            cls.dispatchers[token] = Dispatcher()
    @classmethod
    def register_handler(cls, token, method, *filters):
        cls.dispatchers[token].message.register(method, *filters)
    @classmethod
    def cretae_polling_tasks(cls):
        tasks = []
        for token, disp in cls.dispatchers.items():
            tasks.append(disp.start_polling(cls.bots[token]))
        return tasks