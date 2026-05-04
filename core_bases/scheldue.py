import abc
from typing import List, Dict
from scheldue_data_classes import Lesson, Day, Group
import aiohttp
import asyncio
import threading
from datetime import datetime, date
import time
from abc import ABC, abstractmethod 
# ИНТЕРФЕЙСЫ ПАТЕРНОВ

class Observer(ABC):
    @classmethod
    def register_as_observer(cls):
        ScheldueGetter.get_instance().register_observer(cls)
    @classmethod
    @abstractmethod
    def updates(cls, changes:Dict[str,List]):
        pass

class Subject(ABC):
    observers: List[Observer] = []
    @abstractmethod
    def register_observer(self, o: Observer):
        pass
    @abstractmethod
    def remove_observer(self, o: Observer):
        pass
    @abstractmethod
    def notify_observers(self, changes):
        pass

# ТОЧКА ДОСТУПА К ДАННЫМ РАСПИСНАИЯ

class ScheldueGetter(Subject):
    schedule: Dict[str,List[Lesson]] = {} #ключ - дата, значени - список уроков
    _instance: "ScheldueGetter" = None
    __thread = None
    __schedule_changes: Dict[str,List] = {} # формат как у scheldue
    __groups: List[Group] = []
    __days: List[Day] = []
    __has_scheldue = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            #loop = asyncio.new_event_loop()
            #loop.run_until_complete(cls._instance.refresh_schedule())#первичное обновление расписания чтобы не инициировать обьект с пустым расписанием

            cls._instance.__thread = threading.Thread(target=cls._instance.refresh_timer, daemon=True)# таймер обновлений расписнаия который завершится вместе с основным потоком
            cls._instance.__thread.start()

            return super().__new__(cls)
        raise TypeError("Повторный вызов конструктора невозможен. Для получения экземпляров используйте статичный метод: ScheldueGetter.get_instance()")
    
    @classmethod
    def get_instance(cls):# вызывать вместо конструктора
        if cls._instance is None:
                cls._instance = cls.__new__(cls)
        return cls._instance
    
    def refresh_timer(self, minuts = 1):
        print("Запуск таймера...")
        async def timer():
            while True:
                await asyncio.sleep(minuts*60)
                await self.refresh_schedule()
                print("Расписание обновлено")
        loop = asyncio.new_event_loop()
        loop.create_task(timer())
        loop.run_forever()#запускаем цикл событий навсегда
    @property
    def scheldue(self):
        if self.__has_scheldue:
            return self.schedule
        else:
            while not self.__has_scheldue:
                time.sleep(1)
            return self.schedule
    @property
    def groups(self):
        self.__refresh_groups()
        return self.__groups
    @groups.setter
    def groups(self, value):
        self.groups = value

    def register_observer(self, o: Observer):
        print(f"Зарегистрирован: {o}")
        if o not in self.observers:
            self.observers.append(o)
    def remove_observer(self, o: Observer):
        if o in self.observers:
            self.observers.remove(o)
    def notify_observers(self, changes:List):
        for o in self.observers:
            o.updates(changes)
        
    async def refresh_schedule(self):
        for v in self.__schedule_changes.values(): # отчищаем старые изменения
            v.clear()

        async with aiohttp.ClientSession() as session:
            await self.__refresh_days(session) # обновляем дни
            lsn_dates = self.schedule.keys() # получаем дни
            for day in self.__days: #для каждого дня
                new_lessons = await self.__get_new_Lessons(day.date, session)# получаем уроки по датe
                if day.date in lsn_dates: # если расписание на этот день уже было 
                    if self.schedule[day.date] != new_lessons: # если уроки не совпадают
                        self.__change_schedule(day.date, new_lessons)  # заменяем уроки
                else:
                    self.schedule[day.date] = new_lessons                  # если вообще не было такого дня добавляем уроки
                    self.__schedule_changes[day.date] = new_lessons.copy() # сохраняем что доваили расписание на новый день

        self.__has_scheldue = True
        
        for i in self.__schedule_changes.values():
            if i is not []: # если есть изменения
                self.notify_observers(self.__schedule_changes) # уведомляем об изменениях
                break
 
    def __check_dates(self):
        # устарела ли дата
        def is_outdated(olddate:str, cdate:List[int]):
            # парсим переданную дату
            d = [int(i) for i in olddate.split(".")]
            # и сравниваем 
            for i in range(3):
                if d[i]!=cdate[i]:
                    return True
            else: return False
        def cretate_cur_date():  
            #создаем список текущей даты
            cur_date = date.today()
            cur:list = list()
            cur.append(int(str(cur_date.day)))
            cur.append(int(str(cur_date.month)))
            cur.append(int(str(cur_date.year)))
        cd = cretate_cur_date()
        for d in self.schedule.keys():
            if is_outdated(d, cd):
                od = self.schedule.pop(d)

    def __change_schedule(self, date:str, changed:List): # возвращет разницу расписнаний
        self.__schedule_changes[date].clear() # удаляем прошлые изменения

        if len(self.schedule[date]) == len(changed):  # изменили
            for i in range(len(changed)):
                if self.schedule[date][i] != changed[i]:# ищем все измененные записи
                    self.__schedule_changes[date].append(changed[i])
        else:
            if len(self.schedule[date]) > len(changed):# убавили
                for i in range(len(self.schedule[date])-len(changed)):
                    self.__schedule_changes[date].append(self.schedule[date][-(i+1)])# сохраняем все убавленные
                for i in range(len(changed)):
                    if self.schedule[date][i] != changed[i]:# ищем все измененные записи
                        self.__schedule_changes[date].append(changed[i])

            if len(self.schedule[date]) < len(changed):# прибавили
                for i in range(len(changed)-len(self.schedule[date])):
                    self.__schedule_changes[date].append(changed[-(i+1)])# сохраняем все добавленные
                for i in range(len(self.schedule[date])):
                    if self.schedule[date][i] != changed[i]:# ищем все измененные записи
                        self.__schedule_changes[date].append(changed[i])
        self.schedule[date] = changed #  применяем изменения
        
    async def __get_new_Lessons(self, full_date:str, session: aiohttp.ClientSession)->List[Lesson]:# возвращает список уроков на указанный день
        actual_dates = await session.get("https://api.codescript.site/schedule/getByDate", params={'date':full_date})# получить файл на этот день
        schedule = await actual_dates.json()
        new_lessons:List[Lesson] = list()
        for group in schedule["groups"]: # для каждой группы
            for lesson in group["lessons"]: # каждый урок
                new_lessons.append(Lesson(lesson=lesson, group= group.get("name")))# для этой группы
        return new_lessons #список уроков на этот день
    
    async def __get_new_Days(self, session: aiohttp.ClientSession)->List[Day]:#возвращает список дней на которые есть расписание 
        actual_dates = await session.get("https://api.codescript.site/file/getActualDates")
        schedule = await actual_dates.json()
        new_days:List[Day] = list()
        for day in schedule["actual_dates"]: 
            new_days.append(Day(day["full"]))
        return new_days
    
    async def __refresh_days(self, session):# обновляет записи в поле класса на актуальные
        self.__days = await self.__get_new_Days(session)
    
    async def __get_new_Groups(self, session: aiohttp.ClientSession)->List[Group]:# возвращает список актуальных групп
        actual_dates = await session.get("https://api.codescript.site/general/getGroupNames")
        groups = await actual_dates.json()
        new_groups:List[Group] = list()
        for group in groups["group_names"]: # для каждой группы
            new_groups.append(Group(group))
        return new_groups
    
    async def __refresh_groups(self, session):# обновляет записи в поле класса на актуальные
        self.__groups = await self.__get_new_Groups(session)

if __name__ == "__main__":
    print("hi")
    # class A(Observer):

    #     def update(self, changes):
    #         print("updated")
    # b = A()

    # a = ScheldueGetter.get_instance()
    # print(a.observers)

    #s = [str(v) for v in a.schedule["18.3.2026"]]
    #print(s)
