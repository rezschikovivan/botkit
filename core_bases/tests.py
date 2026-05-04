from abot import ClsHandler, set_handlers_registrator, start_bots, VKBottleComponent, Handler, Filter, Actions, AiogramComponent
from scheldue import Observer

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
    __TOKEN__ = "vk1.a.pbtjqD3lTctuA-OC6_Gi78lySLMZFVzc0bpUta78beFz8ehlF7rAzQL2F7F8Y6CIOT_YaE4O680zd05dZiHiuigrKnpPZYZ7-3JxLC1ZufcLGPo-WU8WLcw2wzbJksRzGwivmTR9OD7f56TkXJ3bdBeUKgi8zdoEbnVhMvlV9F-p4g8s9ghB2Nu3g8xbNxOl_O1rR0_strG3A1k4AXkfNw"

    @Handler(Filter().in_text("hi"))
    async def cab2(message):
        await Actions.answer(message, "!!!!")
    @Handler(Filter().text("hello"))
    async def cab3(message):
        await Actions.answer(message, "Кфбинет №9")

class TGEcho(Echo, AiogramComponent):
    __TOKEN__ = "8397880073:AAFTQ8EN4_ZbCvnBfO_zQ3v_365IpJFeJMI"

    @Handler(Filter().in_text("hi"))
    async def cab2(message):
        await Actions.answer(message, "&&&&&")
    @Handler(Filter().text("hello"))
    async def cab3(message):
        await Actions.answer(message, "Кфбинет №22")

import asyncio
print("works")
#asyncio.run(start_bots())
asyncio.run(VKBottleComponent.cretae_polling_tasks()[0])
