import time
t1 = time.time()

from abot import Filter, Handler, BaseMsg, Sender
from abot.aiogram_component import AiogramComponent

t2 = time.time()
print(t2-t1)

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

# set_handlers_registrator(F)

class Echo():
    @Handler(Filter().in_text("Привет"))
    async def cab1(message:BaseMsg):
        await message.answer("Hello")
        print(type(message))
        print(message.text)

    @Handler(Filter().in_text("name2"))
    async def cab8(message:BaseMsg):
        await message.answer(message, "Вы воспользовались кнопкой!")

class VKEcho(Echo, AiogramComponent):    
    TOKEN = tgram_token

    #@Handler()
    #async def cab2(message):
        #Actions.get_msg(message).sender
        #user = await Actions.get_msg(message).sender#, await Actions.get_msg(message).sender.last_name)
        #print(user.first_name)
        # print("ФОТО:  ", Actions.get_msg(message).photo)
        # print("ДОКУМЕНТ:  ", Actions.get_msg(message).document)
        # print("АУДИО:  ", Actions.get_msg(message).audio)
        # print("ГОЛОСОВОЕ:  ",Actions.get_msg(message).voice)
        # print("ВИДЕО:  ", Actions.get_msg(message).video)
        # print("ТЕКСТ:  ", Actions.get_msg(message).text)
        # print("data:  ", Actions.get_msg(message).date)


# class TGEcho(Echo, AiogramComponent):
#     TOKEN = tgram_token

#     @Handler(Filter().in_text("hi"))
#     async def cab2(message):
#         await Actions.send_inline_kboard(message, keyboard=Keyboard([ [["name", "adata"], ["name","data"]] ]),text="инлайн клавиатура")
#     @Handler(Filter().text("hello"))
#     async def cab3(message):
#         await Actions.answer(message, "Кфбинет №22")

import asyncio
print("works")
#asyncio.run(start_bots())
asyncio.run(AiogramComponent.cretae_polling_tasks()[0])
