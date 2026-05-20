import time

from abot.aiogram_component import AiogramComponent
t1 = time.time()
from abot import Filter, Handler, start_bots, ClsHandler, set_handlers_registrator, BaseMsg, Keyboard
from abot.vkbottle_component import VKBottleComponent
t2 = time.time()
print(t2-t1)

from scheldue_bot.scheldue import Observer, ScheldueGetter
from datetime import datetime, date
import tokens

vk_token = tokens.vk_token

class ScheldueClsHandler(ClsHandler):
    
    def before(cls, mcs, name, bases, attrs:dict):
        if attrs.get("updates") is None: raise AttributeError(f"релизуйте метод updates в {name}")
        attrs["updates"] = classmethod(attrs["updates"])
        return super().before(mcs, name, bases, attrs)
    
    def after(cls, new_cls:Observer, mcs, name, bases, attrs):
        new_cls.register_as_observer()
        return super().after(new_cls, mcs, name, bases, attrs)
set_handlers_registrator(ScheldueClsHandler())

import tokens

class CabsScheldue(Observer):
    scheldue = ScheldueGetter.get_instance()
    all_cabs = ['308', '309', '310', '311', '312', '313', '314', '815', '316', '317', '318', '319', '320', '321', 
                '023', '021', '019', '016', '017', '013', '007', '112', '105', '110', '103', '108', '101', '106', '104',
                '229', '226', '227', '225', '222', '220', '218', '219', '217', '215', '213', '316', '214', '212', '211', '209', '210', '208', '207', '206', '205', '204', '203', '202', '201', '200', 
                '421', '419', '424', '422', '417', '420', '415', '418', '416', '413', '414', '411', '409', '412', '410', '407', '408', '406', '405', '404', '402', '403', '401', '400']
    today_free_cabs = []

    def updates(cls, changes):
        pass
    @classmethod
    def get_free_cabs_now(cls, para:int):
        today_scheldue = cls.scheldue.get_today()
        cls.today_free_cabs = cls.all_cabs.copy()
        for lsn in today_scheldue:
            if lsn.para == para:
                for cab in lsn.cabs:
                    try:
                        i = cls.today_free_cabs.index(cab)
                        cls.today_free_cabs.pop(i)
                    except Exception as e:
                        print(e)
        return cls.today_free_cabs
    
    @Handler(Filter().func(lambda x : any(char.isdigit() for char in x.text)))
    async def send_free_cabs2(cls, message:BaseMsg):
        para = 0
        for character in message.text:
            if character.isdigit():
                para = character
                break   
        await message.answer(cls.get_free_cabs_now(int(para)))

    @Handler(Filter().in_text("кабинет"))
    async def send_free_cabs1(cls, message:BaseMsg):
        await message.send_inline_kboard(Keyboard([ ["1", "1"], ["2", "2"], ["3", "3"], ["4", "4"], ["5", "5"] ], [ ['6', "6"],['7', "7"], ['8', "8"], ['9', "9"] ]), "Выберите пару:")

class VKCabsScheldue(CabsScheldue, VKBottleComponent):    
    TOKEN = tokens.vk_token
    def updates(cls, changes):
        pass
class AiogramCabsScheldue(CabsScheldue, AiogramComponent):
    TOKEN = "8397880073:AAGg_LPBIr3Dlg3z1eMc0187wUU_kKZcY7I"
    def updates(cls, changes):
        pass
    
import asyncio
print("works")
asyncio.run(start_bots())