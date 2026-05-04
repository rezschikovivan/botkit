from abot.core import BaseComponent, ABCFilter
from abot.messaging import ABCMessager
from typing import Dict
import vkbottle
import asyncio
from vkbottle.dispatch.rules.base import AttachmentTypeRule
from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message


class VKFilter(ABCFilter):
    """Реализует работу с фильтрами vkbottle"""
    def func(self, f):
        class CustomRule(ABCRule[Message]):
            def __init__(self, *func: callable):
                self.func = func

            async def check(self, event: Message)->bool:
                for f in self.func:
                    if f(event): continue
                    return False
                else: return True
        return CustomRule(f)
    def photo(self):
        return AttachmentTypeRule("photo")
    
class VKMsger(ABCMessager):
    """Реализует взаимодействие спользователем вк (отправка сообщений и прочее)"""
    @classmethod
    def msg_type(cls):
        return Message
    async def answer(self, msg:Message, text):
        await msg.answer(text)
    async def delete(self, msg):
        return await super().delete(msg)
    async def reply(self, msg, text):
        return await super().reply(msg, text)
    async def send_inline_kboard(self, msg, text, callback=None, url=None):
        return await super().send_inline_kboard(msg, text, callback, url)
    async def send_reply_kboard(self, msg, text, url=None):
        return await super().send_reply_kboard(msg, text, url)

# Класс-регистратор в vkbottle
class VKBottleComponent(BaseComponent):
    bots:Dict[str,vkbottle.Bot] = {}
    @classmethod
    def get_filter(cls):
        return VKFilter()
    @classmethod
    def get_messager(cls):
        return VKMsger()
    @classmethod
    def add_bot(cls, token:str):
        if not token in cls.bots.keys():
            cls.bots[token] = vkbottle.Bot(token=token)
    @classmethod
    def register_method(cls, token, method, *filters):
        if filters is None:
            return cls.bots[token].labeler.message_view.handlers.append(FromFuncHandler(method))
        cls.bots[token].labeler.message_view.handlers.append(FromFuncHandler(method, *filters))
    @classmethod
    def cretae_polling_tasks(cls):
        tasks = []
        for bot in cls.bots.values():
            tasks.append(cls.__castom_polling(bot))
        return tasks
    
    async def __castom_polling(bot:vkbottle.Bot, sleep_time:float=0.01):
        while True:
            async for event in bot.polling.listen():
                for update in event.get("updates"):
                    await bot.router.route(update, bot.polling.api)
            await asyncio.sleep(sleep_time)