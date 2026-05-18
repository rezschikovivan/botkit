#ЗДЕСЬ Я ПРОВЕРЯЮ РАЗЛИЧНЫЙ КОД

# # Многопоточно

# # def background_logger():
# #      while True:
# #          time.sleep(2)
# #          print("refreshed")
 
# # def main_task():
# #     t = threading.Thread(target=background_logger, daemon=False)
# #     t.start()

# # def refrehs():
# #     main_task()

# # refrehs()
# # time.sleep(1.2)

# #main_task(logs)

# # ИТОГО:
# # Каждый поток работает независимо и никак не отражается на работе оснонвого (!возможна гонка данных)
# # Если существуют не демон потоки, то основной будет ждать и завершения иначе он завершится с основным потоком (по умолчанию не домоны)

# # Ассинхронно

# # import threading
# # import time
# # import asyncio

# # async def fun1(x):
# #     while True:
# #         await asyncio.sleep(3)
# #         print('fun1 завершена')


# # async def fun2(x):
# #     while True:
# #         await asyncio.sleep(5)
# #         print('fun2 завершена')


# # async def main():
# #     task1 = asyncio.create_task(fun1(4))
# #     task2 = asyncio.create_task(fun2(4))

# #     await task1
# #     await task2
# #     print("main")


# # print(time.strftime('%X'))

# # asyncio.run(main())
# # print("main1")

# # print(time.strftime('%X'))

# # ИТОГО:
# # управление передается циклу событий а там между задачами в цикле событий пока они все не будут завершены (основной поток ждет завершения цикла событий), но
# # в то же время управление между задачами внутри цикла событий может передаваться (результат практически как параллелльно и все благодоря await).

# # переписать обновление распиания под синхронную версию работающую в отдельном потоке
# #from core import Component
# #from scheldue import ScheldueGetter
# # from typing import List

# # s = "hpo"

# # # a = ScheldueGetter()
# # # b = ScheldueGetter()

# # # class B(Component):
# # #     def hello():...
# # #     y = 5
# # #     __TOKEN__ = "hello"


# # a = "18.3.2026"
# # from datetime import datetime, date
# # # устарела ли дата
# # def is_outdated(d:str):
# #     # парсим переданную дату
# #     d = d.split(".")
# #     d = [int(i) for i in d]
# #     #создаем список текущей даты
# #     cur_date = date.today()
# #     cur:list = list()
# #     cur.append(int(str(cur_date.day)))
# #     cur.append(int(str(cur_date.month)))
# #     cur.append(int(str(cur_date.year)))
# #     for i in range(3):
# #         if d[i]!=cur[i]:
# #             return True
# #     else: return False

    

# #print(is_outdated(a))
    
# #print(parse_date(a))
# # import abc
# # class A(abc.ABC):
# #     @classmethod
# #     @abc.abstractmethod
# #     def foo(cls):
# #         print("foo")

# #     def bar (): pass

# # class B(A):
# #     ...

# # #print([i for i in A.__dict__.keys() if not i.startswith("__")])
# # print(type(A.foo))
# # import aiogram

# # token = "8597992462:AAHguxk307-4sBK1JYGnBGCT_rn_lPgz1Lg"
# # bot = aiogram.Bot(token=token)
# # dp = aiogram.Dispatcher()

# # async def echo(message: aiogram.types.Message):
# #         await bot.send_message(message.chat.id, "GHbhb")
# #         print("ho")

# # dp.message.register(echo)
# # print(dp.message.handlers)
# # asyncio.run(dp.start_polling(bot))


# # class A():
# #     def __call__(self, func, *args, **kwds):
# #         def wrapper():
# #             print(1)
# #             func()
# #             print(2)
# #         return wrapper
# # @A()
# # def foo():
# #     """Return a friendly greeting."""
# #     print("Hi")
# # foo()


# # from vkbottle.bot import Bot, Message, BotLabeler
# # from vkbottle import ABCPolling, BotPolling, LoopWrapper
# # import asyncio

# # loop_wrapper = LoopWrapper()
# # bot = Bot(
# #    "vk1.a.pbtjqD3lTctuA-OC6_Gi78lySLMZFVzc0bpUta78beFz8ehlF7rAzQL2F7F8Y6CIOT_YaE4O680zd05dZiHiuigrKnpPZYZ7-3JxLC1ZufcLGPo-WU8WLcw2wzbJksRzGwivmTR9OD7f56TkXJ3bdBeUKgi8zdoEbnVhMvlV9F-p4g8s9ghB2Nu3g8xbNxOl_O1rR0_strG3A1k4AXkfNw",
# #    loop_wrapper=loop_wrapper
# #    )

# # #@bot.on.message()
# # async def handle_message(message):
# #     await message.answer(f"Получено: {message.text}")

# # # Получаем объект корутины

# # # Основная функция для запуска бота ВКонтакте 
# # async def run_vk_bot(): 
# #     await bot.run_polling() 

# # async def hello():
# #     for i in range(10):
# #         print("HI")
# #         await asyncio.sleep(5)



# # # Главная функция 
# # def main():
# #     tasks = [ 
# #     #### Будет еще логика 
# #         hello(),
# #         run_vk_bot(),
# #     ] 
# #     for task in tasks:
# #         loop_wrapper.add_task(task)
# #     loop_wrapper.run()
 
# # if __name__ == "__main__": 
# #     print(11)
# #     main()
# #     print(22)
# # from abc import ABC, abstractmethod
# # from types import LambdaType

# # class Handler():
# #     def __init__(self, *filters: LambdaType):
# #         self.filters = filters
# #         self.is_set = False
# #     def __call__(self, func = None, *args, **kwds):
# #         if not self.is_set:
# #             self.func = func
# #             self.is_set = True
# #             return self
# #         return  self.func(*args, **kwds)     

# class A :
# #    @Handler(lambda m: "hi" in m)
#     def echo():
#         print("echo")
#         return("privet")
    
# class AB:
# #    @Handler(lambda m: "hi" in m)
#     def hello():
#         print("echo")
#         return("privet")
# # h = Handler()
# # a = A()
# # print(Handler.__qualname__)
# # print(A.__qualname__)
# a = A.echo
# A.echo = AB.hello

# # d1 = {"a":1,"b":2,"c":3}
# # d2 = {"a":11,"w":22,"v":33}
# # d3 = {"v":111,"f":222,"g":333}
# # d1.update(d2)
# # d1.update(d3)
# #print(a.__qualname__)

# class FilterMethods():
#     @property
#     def text(self):return"1"
#     @text.setter
#     def text(self, text):pass
#     @property
#     def in_text(self):pass
#     @in_text.setter
#     def in_text(self, text):pass
#     @property
#     def cmnd(self):pass
#     @cmnd.setter
#     def cmnd(self, text):pass

# class Filter(FilterMethods):
#     #через фабрику получаем экземпляр имплементора
#     @property
#     def filter_imp(self):return self.__filter_imp
# #     @filter_imp.setter
# #     def filter_imp(self, new): self.__filter_imp = new
# #     @property
# #     def text(self):
# #         return super().text
# #     @property
# #     def in_text(self):pass
# #     @in_text.setter
# #     def in_text(self, text): return lambda x : text in x.text
# #     @property
# #     def cmnd(self):pass
# #     @cmnd.setter
# #     def cmnd(self, text): return lambda x : x.text == f"/{text}"
# class ClassProperty:
#     def __init__(self, prop):
#         self.func = prop
#     def __get__(self, inst, klass=None):
#         if klass is None:
#             klass = type(inst)
#         return self.func(klass)
# def classproperty(func):
#     return ClassProperty(func)

# import abc
# class A0(abc.ABC):
#     @classproperty
#     @abc.abstractmethod
#     def foo(cls):
#         return "hello"
# class A1(A0):
#     @classproperty
#     def foo(cls):
#         return super().foo
# print(A0.foo)
# from typing import List, Any, Dict, Iterable
# class Button():
#     def __init__(self, row:int, column:int, text:str, action:str|Dict):
#         self.row = row
#         self.column = column
#         self.text = text
#         self.action = action

# class Keyboard():

#     def __init__(self, frame:List[List[str,str]]):
#         """Во frame принимается многомерный список, внутри которого каждый список определяет строку и кол-во эл-ов в ней.
#          Внутри 'структурирующих' списков первым указывается название кнопки и затем действие. По умолчанию действие это отправка текста, 
#          если будет указанна ссылка, то при нажатии будет осуществлённ переход. Также можно указать callback, он указываетя 2-м эл-ом
#           списка как значение словаря под любым ключом. """
#         self.buttons:List[Button] = []
#         self.check(frame)
#         print(self.buttons)

#     def check(self, iterable:Iterable, row=-1, column=-1):
#         for i in iterable:
#             row += 1
#             if isinstance(i[0], list):
#                 self.buttons.extend(self.check(i, row, column+1))
#             else:
#                 self.buttons.append(Button(row, column, i[0],i[1]))
# Keyboard([ [ [1,2],[1,2] ],  [ [1,2],[1,2] ] ])
#mport abot.utils
# from vkbottle import Bot, GroupEventType, GroupTypes, Callback
# from vkbottle.bot import Message
# from vkbottle import Keyboard, Callback
# from vkbottle.modules import json
# import tokens
# from vkbottle.dispatch.rules.base import PayloadRule

# TOKEN = tokens.vk_token
# bot = Bot(token=TOKEN)

# @bot.on.message(text="меню")
# async def show_menu(message: Message):
#     keyboard = (
#         Keyboard()
#         .add(Callback("Привет", {"action": "hello"}))
#         .add(Callback("Пока", {"action": "bye"}))
#     )
#     await message.answer("Нажмите кнопку:", keyboard=keyboard)


# @bot.on.message(PayloadRule({"action": "hello"}))
# async def show_menu_handler(event):
#     print("22")
#     await bot.api.messages.send_message_event_answer(
#             event_id=event.event_id,
#             user_id=event.user_id,
#             peer_id=event.peer_id,
#             answer_data={"type": "show_snackbar", "text": "Привет! Рад вас видеть!"}
#         )

# @bot.on.message(PayloadRule({"action": "bye"}))
# async def buy_item_handler(message):
#     print(3333)
#     # Логика покупки товара
#     await message.answer("ehff")

# if __name__ == "__main__":
#     print("works")
#     bot.run_forever()



# bot = Bot(token=TOKEN)
# lab = bot.labeler

# @bot.on.message(text="меню")
# async def show_menu(message: Message):
#     keyboard = (
#         Keyboard()
#         .add(Callback("Старт", {"action": "start"}))
#         .add(Callback("Помощь", {"action": "help"}))
#         .add(Callback("Настройки", {"action": "settings", "user_id": message.from_id}))
#     )
#     await message.answer("Главное меню:", keyboard=keyboard)

# # Обработчик для кнопки "Старт"
# @bot.on.raw_event(GroupEventType.MESSAGE_EVENT, GroupTypes.MessageEvent, PayloadRule({"action": "start"}))
# async def start_button_handler(message: Message):
#     print(7897941)
#     await message.answer("Вы нажали кнопку Старт! Начинаем работу...")


# if __name__ == "__main__":
#     print(1)
#     bot.run_forever()
# class B:
#     def foo(self):
#         print(self.slot)

# class A:
#     # def __init__(self):
#     #     print("ii")
#     def __foo__(self): return "text"

#     def __get__(self, instance, owner):
#         print("get")

#     def __getattribute__(self, name):
#         print("attribute ", name)
#         if name == "__foo__":
#             def wrapper(func):
#                 def y(x): return x*2
#                 return y
#             return wrapper(super().__getattribute__(name))
#         return super().__getattribute__(name)

# print(A().__foo__(5))
a = [308, 309, 310, 311, 312, 313, 314, 815, 316, 317, 318, 319, 320, 321, '023', '021', '019', '016', '017', '013', '007', 112, 105, 110, 103, 108, 101, 106, 104, 229, 226, 227, 225, 222, 220, 218, 219, 217, 215, 213, 316, 214, 212, 211, 209, 210, 208, 207, 206, 205, 204, 203, 202, 201, 200, 421, 419, 424, 422, 417, 420, 415, 418, 416, 413, 414, 411, 409, 412, 410, 407, 408, 406, 405, 404, 402, 403, 401, 400]
A = map(str, a)
print(list(A))
