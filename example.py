import time

from botkit.core import ClsHandler, set_handlers_registrator

t1 = time.time()

from botkit import Filter, Handler, BaseMsg, Sender, Keyboard, start_bots
from botkit.vkbottle_component import VKBottleComponent
from botkit.aiogram_component import AiogramComponent

t2 = time.time()
print(t2-t1)

import tokens

vk_token = tokens.vk_token
tgram_token = tokens.tgram_token

# Если нужно, можно создать свой класс-хэндлер, который будет выполнять какие-то действия при регистрации методов, например, проверять наличие определенных атрибутов или автоматически регистрировать методы в каком-то реестре. Для этого нужно создать класс, наследующийся от ClsHandler, и реализовать методы before и after. Метод before будет вызываться перед созданием класса-хэндлера, а метод after - после создания класса-хэндлера. В этих методах можно выполнять любые необходимые действия с классом-хэндлером или его атрибутами. Но важно возвращать результат вызова родителя, чтобы не нарушать логику работы ядра. 
class F(ClsHandler):

    def before(cls, mcs, name, bases, attrs):
        print(f"Создается класс-хэндлер {name}...")
        return super().before(mcs, name, bases, attrs)
    
    def after(cls, new_cls, mcs, name, bases, attrs):
        print(f"Класс-хэндлер {name} успешно создан!")
        return super().after(new_cls, mcs, name, bases, attrs)

set_handlers_registrator(F())

class Echo:

    @Handler(Filter().in_text("hi"))
    async def cab8(cls, message:BaseMsg):
        await message.answer("Вы воспользовались кнопкой!")

    @Handler(Filter().in_text("Привет"))
    async def cab2(cls, message:BaseMsg):
        await message.send_reply_kboard(keyboard=Keyboard([ [["name1", "data1"], ["name","data2"]] ]),text="реплай клавиатура")

class VKEcho(Echo, VKBottleComponent):    
    TOKEN = vk_token

    @Handler(Filter().text("кабинет"))
    async def cab3(cls, message:BaseMsg):
        await message.answer("Кфбинет №11")
    # Пример метода-хэндлера, который выводит в консоль информацию о сообщении и его отправителе. В этом методе мы получаем объект отправителя сообщения, а также проверяем наличие различных типов вложений (фото, документы, аудио и т.д.) и выводим эту информацию в консоль.
    # @Handler()
    # async def cab2(cls, message:BaseMsg):

    #     user:Sender = await message.sender
    #     print(user.first_name)
    #     print("ФОТО:  ", message.photo)
    #     print("ДОКУМЕНТ:  ", message.document)
    #     print("АУДИО:  ", message.audio)
    #     print("ГОЛОСОВОЕ:  ", message.voice)
    #     print("ВИДЕО:  ", message.video)
    #     print("ТЕКСТ:  ", message.text)
    #     print("data:  ", message.date)


class TGEcho(Echo, AiogramComponent):
    TOKEN = tgram_token

    @Handler(Filter().text("кабинет"))
    async def cab3(cls, message:BaseMsg):
        await message.answer("Кфбинет №22")

import asyncio
print("works")
asyncio.run(start_bots())
