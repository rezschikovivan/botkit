# abot

This framework is designed for writing bots that can use various frameworks to interact with the messenger API.
## Install
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
from abot import Filter, Handler, BaseMsg, Sender, BaseComponent, Keyboard
from abot.vkbottle_component import VKBottleComponent
from abot.aiogram_component import AiogramComponent

class Echo(BaseComponent):
    @Handler(Filter().in_text("Hi"))
    async def greeting(cls, message:BaseMsg):
        await message.answer(message, "Hello!")

    @Handler()
    async def cab2(cls, message:BaseMsg):
        user: Sender = await message.send_inline_kboard
        print(user.first_name)
        print("ФОТО:  ", message.photo)
        print("ДОКУМЕНТ:  ", message.document)
        print("АУДИО:  ", message.audio)
        print("ГОЛОСОВОЕ:  ", message.voice)
        print("ВИДЕО:  ", message.video)
        print("ТЕКСТ:  ", message.text)
        print("data:  ", message.date)

class VKEcho(Echo, VKBottleComponent):    
    TOKEN = vk_token
    @Handler(Filter().in_text("bye"))
    async def cab1(cls, message:BaseMsg):
        await message.answer("goodbye at VK")

class TGEcho(Echo, AiogramComponent):
    TOKEN = tgram_token

    @Handler(Filter().in_text("bye"))
    async def cab2(cls, message:BaseMsg):
        await message.send_inline_kboard(message, keyboard=Keyboard([ [["name1", "data1"], ["name2","data2"]] ]),text="goodbye")

import asyncio
#asyncio.run(start_bots()) run all bots
asyncio.run(VKBottleComponent.cretae_polling_tasks()[0]) # starts only one specific bot from VKBottleComponent
```