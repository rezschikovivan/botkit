from setuptools import setup, find_packages
from botomorph import __version__

  
readme_literal = """
# botomorph

This framework is designed for writing bots that can use various frameworks to interact with the messenger API.
## Install

```
pip install botomorph
```

GitHub: https://github.com/rezschikovivan/botomorph 

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
from botomorph import Filter, Handler, BaseMsg, Sender, Keyboard, start_bots
from botomorph.vkbottle_component import VKBottleComponent
from botomorph.aiogram_component import AiogramComponent

# If necessary, you can create your own handler class that will perform certain actions when methods are registered, such as checking for the presence of specific attributes or automatically registering methods in a registry. To do this, you need to create a class that inherits from ClsHandler and implement the before and after methods. The before method will be called before the handler class is created, and the after method will be called after the handler class is created. These methods allow you to perform any necessary actions with the handler class or its attributes. However, it is important to return the result of the parent call to avoid breaking the core's logic. 
class F(ClsHandler):

    def before(cls, mcs, name, bases, attrs):
        print(f"A handler class is being created {name}...")
        return super().before(mcs, name, bases, attrs)
    
    def after(cls, new_cls, mcs, name, bases, attrs):
        print(f"The {name} handler class has been successfully created!")
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

    # An example of a handler method that displays information about the message and its sender in the console. In this method, we retrieve the sender object of the message and check for different types of attachments (photos, documents, audio, etc.), displaying this information in the console.
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
Basic functionality is now available using aiogram and vkbottle. It currently lacks features such as inline_buttons and FSM, but it is ideal for writing bots that do not require complex user interaction but still support multi-platform
"""




setup(
  name='botomorph',
  version = __version__,
  author='rezschikovivan',
  author_email='rezschikovivan@gmail.com',
  description='Framework to creating bots',
  long_description=readme_literal,
  long_description_content_type='text/markdown',
  url='https://github.com/rezschikovivan/botomorph',
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
  keywords='botomorph bot bots asynchronous framework aiogram vkbottle',
  project_urls= {},
  python_requires='>=3.12.0'
)