from abot import ClsHandler, set_handlers_registrator, start_bots, VKBottleComponent, Handler, Filter, Actions, AiogramComponent, Keyboard
from scheldue import Observer

import tokens

vk_token = tokens.vk_token
tgram_token = tokens.tgram_token

# ПРИМЕР ИСПОЛЬЗОВАНИЯ. ТЕСТОВ ПОКА НЕТ...

# class F(ClsHandler, ABC):
#     @classmethod
#     def before(cls, mcs, name, bases, attrs):
#         if attrs.get("updates") is None: raise AttributeError(f"релизуйте метод updates в {name}")
#         attrs["updates"] = classmethod(attrs["updates"])
#     @classmethod
#     def after(cls, new_cls:Observer, mcs, name, bases, attrs):
#         new_cls.register_as_observer()

#set_handlers_registrator(F)

class Echo():
    @Handler(Filter().in_text("прив"))
    async def cab1(message):
        await Actions.answer(message, "Рад видеть!")

class VKEcho(Echo, VKBottleComponent):    
    __TOKEN__ = vk_token

    @Handler(Filter().in_text("hi"))
    async def cab2(message):
        await Actions.send_reply_kboard(message, text="инлайн клавиатура", keyboard=Keyboard([ [["name1", "https://zvuk.com/track/176947994"], ["name2",{"clb":"data"}]] ]))
    @Handler(Filter().text("hello"))
    async def cab3(message):
        await Actions.answer(message, "Кфбинет №9")

class TGEcho(Echo, AiogramComponent):
    __TOKEN__ = tgram_token

    @Handler(Filter().in_text("hi"))
    async def cab2(message):
        await Actions.send_inline_kboard(message, text="инлайн клавиатура", keyboard=Keyboard([ [["name", "adata"], ["name","data"]] ]))
    @Handler(Filter().text("hello"))
    async def cab3(message):
        await Actions.answer(message, "Кфбинет №22")

import asyncio
print("works")
#asyncio.run(start_bots())
asyncio.run(VKBottleComponent.cretae_polling_tasks()[0])
