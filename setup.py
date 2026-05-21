from setuptools import setup, find_packages
from abot import __version__

  
readme_literal = """
# abot

This framework is designed for writing bots that can use various frameworks to interact with the messenger API.
## Install

```
pip install abot
```

Download from: https://github.com/rezschikovivan/abot 

## Why use

The framework allows you to run bots written in it on different platforms, using different frameworks to interact with their APIs. The class-based approach to writing handlers allows you to use inheritance to extract common logic or define a family of similar bots.

## Features
- Multiplatform bots
- Inheritance of handlers
- A class-based approach to writing bots
- Has type hints
- Asynchronous

## Example

```
from abot import Filter, Handler, BaseMsg, Sender, Keyboard, start_bots
from abot.vkbottle_component import VKBottleComponent
from abot.aiogram_component import AiogramComponent

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
```

## summary
Basic functionality is now available using aiogram and vkbottle. It currently lacks features such as inline_buttons and FSM, but it is ideal for writing bots that do not require complex user interaction. 
"""




setup(
  name='abot',
  version = __version__,
  author='rezschikovivan',
  author_email='rezschikovivan@gmail.com',
  description='Framework for creating bots',
  long_description=readme_literal,
  long_description_content_type='text/markdown',
  url='https://github.com/rezschikovivan/abot',
  packages=find_packages(),
  install_requires=[
    'vkbottle==4.8.0', 
    'aiogram==3.27.0'
    ],
  classifiers=[
    'Programming Language :: Python :: 3.14',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='abot bot bots asynchronous',
  project_urls= {},
  python_requires='>=3.12.0'
)