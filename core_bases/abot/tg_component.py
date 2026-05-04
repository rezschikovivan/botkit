from abot.core import BaseComponent, ABCFilter, ABCMessager
from aiogram.types import Message
from typing import Dict
from aiogram.filters import BaseFilter 
import aiogram

class CustomFilter(BaseFilter):
    def __init__(self, *func: callable):
        self.func = func

    def __call__(self, event)->bool:
        for f in self.func:
            if f(event): continue
            return False
        else: return True

class AiogramFilter(ABCFilter):
    def func(self, f):
        return CustomFilter(f)
    
class AiogramMsger(ABCMessager):
    @classmethod
    def msg_type(cls):
        return Message
    async def answer(msg:Message, text):
        return await msg.answer(text)

# Класс-регистратор в aiogram
class AiogramComponent(BaseComponent):
    bots:Dict[str,aiogram.Bot] = {}
    dispatchers: Dict[str,aiogram.Dispatcher] = {}
    @classmethod
    def get_filter(cls):
        pass
    @classmethod
    def get_messager(cls):
        pass
    @classmethod
    def add_bot(cls, token:str):
        if not token in cls.bots.keys():
            cls.bots[token] = aiogram.Bot(token=token)
            cls.dispatchers[token] = aiogram.Dispatcher()
    @classmethod
    def register_method(cls, token, method, *filters):
        cls.dispatchers[token].message.register(method, *filters)
    @classmethod
    def cretae_polling_tasks(cls):
        tasks = []
        for token, disp in cls.dispatchers.items():
            tasks.append(disp.start_polling(cls.bots[token]))
        return tasks
    


    