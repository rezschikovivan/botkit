from abot.core import BaseComponent, ABCFilter
from abot.messaging import ABCMessager,Button,Sender
import abot.messaging
from typing import Dict, Any
import vkbottle
import asyncio
from vkbottle.dispatch.rules.base import AttachmentTypeRule
from vkbottle.dispatch.handlers import FromFuncHandler
from vkbottle.dispatch.rules import ABCRule
from vkbottle.bot import Message
from vkbottle import Keyboard, OpenLink, Callback, Text

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
    msg:Message# нужно чтобы интерпритатор видел тип поля
    def __init__(self, msg):
        super().__init__(msg)
    @classmethod
    def msg_type(cls):
        return Message
    async def answer(self, msg:Message, text):
        return await msg.answer(text)
    async def delete(self, msg:Message):
        raise RuntimeError("VKBottle пока не умеет удалять сообщения (я не нашел)")
    async def reply(self, msg:Message, text):
        await msg.reply(text)
    async def send_reply_kboard(self, msg, keyboard:Keyboard, text:str|None = None):
        vk_keyboard:Keyboard = Keyboard(True, False)
        self.create_kboard(vk_keyboard, keyboard)
        await msg.answer(text, keyboard=vk_keyboard)
    async def send_inline_kboard(self, msg:Message, keyboard:abot.messaging.Keyboard, text:str|None = None):
        vk_keyboard:Keyboard = Keyboard(False, True)
        self.create_kboard(vk_keyboard, keyboard)
        await msg.answer(text, keyboard=vk_keyboard)
    def create_kboard(self, vk_keyboard:Keyboard, keyboard:abot.messaging.Keyboard):
        row = 0
        for b in keyboard.buttons:
            if b.row == row:
                self.add_button(vk_keyboard, b)
            else:
                row = b.row
                vk_keyboard.row()
                self.add_button(vk_keyboard, b)
    def add_button(self, vk_keyboard:Keyboard, button:Button):
        if button.is_url:
            vk_keyboard.add(OpenLink(button.action, button.text))
        elif button.is_callback:
            vk_keyboard.add(Callback(button.text, {"payload":list(button.action.values())[0]}))
        else: 
            vk_keyboard.add(Text(button.text, {"payload":str(button.action)}))
    @property
    def data(self):
        return self.msg.date
    @property
    def text(self):
        return self.msg.text
    def get_attachment(self, attach_type:str)->Any|None:
        if not self.msg.attachments:
            return None
        attachment = None
        for i in self.msg.attachments:
            if i.type.value == attach_type:
                attachment = i.doc
                break
        else: return None
        return attachment
    @property
    def document(self):
        return self.get_attachment("doc")
    @property
    def audio(self):
        return self.get_attachment("audio")
    @property
    def video(self):
        return self.get_attachment("video")
    @property
    def location(self):
        return self.get_attachment("geo")
    @property
    def voice(self):
        return self.get_attachment("audio_message")
    @property
    def sticker(self):
        return self.get_attachment("sticker")
    @property
    def sender(self):
        user = asyncio.get_running_loop().create_task(self.msg.get_user())

        return Sender(self.msg.from_id, user[0].first_name,user[0].last_name)
    
# Класс-регистратор в vkbottle
class VKBottleComponent(BaseComponent):
    bots:Dict[str,vkbottle.Bot] = {}
    @classmethod
    def get_filter(cls):
        return VKFilter()
    @classmethod
    def get_messager(cls):
        return VKMsger
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