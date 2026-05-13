import time
t1 = time.time()
from abot import Filter, Handler, start_bots, ClsHandler, set_handlers_registrator, BaseMsg
from abot.vkbottle_component import VKBottleComponent
t2 = time.time()
print(t2-t1)

from scheldue import Observer, ScheldueGetter
import tokens

vk_token = tokens.vk_token

class ScheldueClsHandler(ClsHandler):
    def before(cls, mcs, name, bases, attrs):
        super().before(mcs, name, bases, attrs)
        if attrs.get("updates") is None: raise AttributeError(f"релизуйте метод updates в {name}")
        attrs["updates"] = classmethod(attrs["updates"])
    def after(cls, new_cls:Observer, mcs, name, bases, attrs):
        super().after(new_cls, mcs, name, bases, attrs)
        new_cls.register_as_observer()
set_handlers_registrator(ScheldueClsHandler)

class CabsScheldue(Observer):
    @Handler(Filter().cmnd("start"))
    async def start_hndler(message:BaseMsg):
        await message.answer(message, "Рад видеть!")

    @Handler(Filter().in_text("name2"))
    async def cab8(message:BaseMsg):
        await message.answer(message, "Вы воспользовались кнопкой!")

class VKCabsScheldue(CabsScheldue, VKBottleComponent):    
    ...

import asyncio
print("works")
asyncio.run(start_bots())

