import asyncio
from types import NoneType
from typing import Iterable, List, Dict
import aiohttp
import json
import abc

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.filters import Command, command
from aiogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button

bot = Bot(token="8597992462:AAHguxk307-4sBK1JYGnBGCT_rn_lPgz1Lg")
dp = Dispatcher()

@dp.message()
async def add(msg: types.Message):
    cabs = Lesson.split_cabs_row(msg.text)
    try:
        for cab in cabs:
            Cabinets.add_cub(cab)
        print(Cabinets.cabs)
    except WrongValue as e:
        msg.answer(e)
    await msg.answer(str(Cabinets.cabs))















class WrongValue(Exception):
    def __init__(self, message): 
        super().__init__(message) 


def deep_viewing(collection:dict):
        for key,value in collection.items():
            if isinstance(value, Iterable) and not isinstance(value, (str, bytes, list)):
                yield from deep_viewing(value)
            else:
                yield key, value

class ScheduleManager():
    schedule: Dict[str,Day] = {}

    @staticmethod#Добавить день в расписание
    def set_day(day:Day):
        ScheduleManager.schedule[day.full_date] = day

    @staticmethod
    async def refresh_schedule():
        async with aiohttp.ClientSession() as session:
            actualDates = await session.get("https://api.codescript.site/file/getActualDates")
            dates = await actualDates.json()
            #для каждого дня
            for date in dates["actual_dates"]:
                #получаем обьект дня по актуальному расписанию даты
                new_day = await ScheduleManager.get_day(date["full"], session)
                for day in ScheduleManager.schedule.values():
                    #если день с такой датой есть
                    if new_day.full_date == day.full_date:
                        #если расписание не изменилось
                        if new_day == day: 
                            break 
                    #значит такого дня не было или есть изменения - добавить
                else:
                    ScheduleManager.set_day(new_day)

    @staticmethod
    async def get_day(full_date:str, session: aiohttp.ClientSession):
            day = Day(full_date)
            actualDates = await session.get("https://api.codescript.site/schedule/getByDate", params={'date':full_date})# получаtvь файл на этот день
            schedule = await actualDates.json()
            for group in schedule["groups"]: # для каждой группы
                for lesson in group["lessons"]: # каждый урок
                    day.add_lesson(Lesson(lesson))
            return day

    @staticmethod
    async def get_actual_cabs():
        async with aiohttp.ClientSession() as session:
            response = await session.get("https://api.codescript.site/file/getActualDates")
            dates = await response.json()
            # для каждого актуального дня 
            for date in dates["actual_dates"]:
                day = await ScheduleManager.get_day(date, session)#создать актуальный день
                ScheduleManager.set_day(day)

class Cabinets(Iterable):
    fl0 = {"001":[False]*10,"002":[False]*10,"003":[False]*10}
    fl1 = {"100":[False]*10,"101":[False]*10}
    fl2 = {"200":[False]*10,"201":[False]*10}
    fl3 = {"300":[False]*10,"301":[False]*10,"302":[False]*10,"303":[False]*10,"304":[False]*10,"305":[False]*10,"306":[False]*10,"307":[False]*10}
    fl4 = {"400":[False]*10,"401":[False]*10}

    cabs = {
        "Подвал":fl0,
        "1 этаж":fl1,
        "2 этаж":fl2,
        "3 этаж":fl3,
        "4 этаж":fl4
            }
    def __init__(self):
        self.fl0 = {"001":[False]*10,"002":[False]*10,"003":[False]*10}
        self.fl1 = {"100":[False]*10,"101":[False]*10}
        self.fl2 = {"200":[False]*10,"201":[False]*10}
        self.fl3 = {"300":[False]*10,"301":[False]*10,"302":[False]*10,"303":[False]*10,"304":[False]*10,"305":[False]*10,"306":[False]*10,"307":[False]*10}
        self.fl4 = {"400":[False]*10,"401":[False]*10}

        self.cabs = {
        "Подвал":self.fl0,
        "1 этаж":self.fl1,
        "2 этаж":self.fl2,
        "3 этаж":self.fl3,
        "4 этаж":self.fl4
               }
    def __iter__(self):
        return deep_viewing(self.cabs)

    @staticmethod
    def add_cub(new_cab:str):
            flr = Cabinets.get_floors([new_cab])[0]
            if flr is None: return
            Cabinets.cabs[flr][new_cab] = [False]*10

    @staticmethod
    def remove(cab:str):
            flr = Cabinets.get_floors([cab])[0]
            if flr == None: return
            Cabinets.cabs[flr].pop(cab)

    @staticmethod
    def get_floors(cabs:list[str]) -> list[str]:
        resp = []
        for i in cabs:
            if i.isdecimal():
                match(i[0]):
                    case ("0"):
                        resp.append("Подвал") 
                    case ("1"):
                        resp.append("1 этаж") 
                    case ("2"):
                        resp.append("2 этаж") 
                    case ("3"):
                        resp.append("3 этаж") 
                    case ("4"):
                        resp.append("4 этаж")
                    case(_):
                        resp.append(None)
        return tuple(resp)


class Day(Iterable):
    def __init__(self, date:str):
        self.lessons: list[Lesson] = []
        self.full_date = date
        self.cabs = Cabinets.cabs.copy()

    def __str__(self):
        return self.full_date

    def __iter__(self):
        return deep_viewing(self.cabs)

    def __eq__(self, other:Day)->bool:
        if self.full_date != other.full_date or len(self.lessons) != len(other.lessons): return False
        for i in range(len(self.lessons)):
            if self.lessons[i] == other.lessons[i]:
                continue
            return False
        return True

    def __ne__(self, value)->bool:
        return not (self == value)

    def __contains__(self, key:Lesson)->bool:
        for i in self.lessons:
            if i == key:
                return True
        return False

    def add_lesson(self, lesson:Lesson):
        levels = Cabinets.get_floors(lesson.cabinets)
        for i in range(len(lesson.cabinets)):
            cab_arr = self.cabs[levels[i]].get(lesson.cabinets[i], 1)
            if cab_arr == 1:
                raise WrongValue(f"Кабинета указанного в файле как {lesson.cabinets[i]} не существет в боте")
            cab_arr[lesson.index] = True #
            self.lessons.append(lesson)


class Lesson():
    def __init__(self, lessons: dict):
        self.index = lessons.get("index")
        self.discipline = lessons.get("discipline")
        self.group = lessons.get("name")
        self.cabinets = self.split_cabs_row(lessons.get("classroom_raw"))
	
    def __eq__(self, other:Lesson)->bool:
        if len(self.cabinets) != len(other.cabinets): return False
        for i in range(len(self.cabinets)):
            if self.cabinets[i] == other.cabinets[i] and self.index == other.index and self.discipline == other.discipline and self.group == other.group:
                continue
            return False
        return True
    def __ne__(self, value)->bool:
        return not (self == value)

    def get_levels(self) -> list[str]:
        return Cabinets.get_floors(self.cabinets)

    @staticmethod
    def split_cabs_row(rooms:str)-> list[str]:
        rooms = rooms.replace(" ", "")
        if "/" in rooms:
             arr = rooms.split("/")
             rooms = []
             for i in arr:
                 if i.isdecimal():
                     rooms.append(i)
             return rooms
        elif rooms == "": # физкультура помечается как "" у нее нету кабинета
            return []
        else:
             a = [rooms]
             return a


if __name__ == "__main__":
    l1 = Lesson({"index":1,"classroom_raw" : "001"})
    l2 = Lesson({"index":1,"classroom_raw" : "002"})
    l3 = Lesson({"index":1,"classroom_raw" : "003/002"})
    d1 = Day("23.1.2026")
    d1.add_lesson(l1)
    d1.add_lesson(l2)

    d2 = Day("22.1.2026")
    d2.add_lesson(l3)
    ScheduleManager.set_day(d2)
    ScheduleManager.set_day(d1)
    print(len(ScheduleManager.schedule))

    print("До обновления")
    print(ScheduleManager.schedule["23.1.2026"].lessons[0].cabinets)
    print("")


    print("После обновления")
    print("")
    asyncio.run(ScheduleManager.refresh_schedule())
    print(ScheduleManager.schedule["23.1.2026"].lessons[0].cabinets)
    print("")

# asyncio.run(ScheduleManager.get_actual_cabs())