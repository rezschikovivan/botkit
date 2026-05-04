from typing import List, Dict, Any
from datetime import datetime

class Day():
    def __init__(self, date:str, timing:list = None):
        self.__date = date 
        self.__timing = timing
    def __eq__(self, other:"Day") -> bool:
        if isinstance(other, "Day"):
            if  other.date != self.date:
                return False
            return True
        return False
    def __ne__(self, other:"Day")-> bool:
        return not self.__eq__(other)
    @property
    def date(self)->str:
        return self.__date
    @date.setter
    def date(self, value):
        raise NameError("Только чтение")
    @property
    def week_day(self)->str:
        days = ["Понедельник" , "Вторник" , "Среда" , "Четверг" , "Пятница" , "Суббота" , "Воскресенье"]
        return days[datetime.strptime(self.date, r"%d/%m/%Y").weekday()]
    @week_day.setter
    def week_day(self, value):
        raise NameError("Только чтение")
    @property
    def timing(self):
        if self.__timing is None:
            if self.week_day == "Понедельник":
                return ["8:15 - 9:45", "10:05 - 10:50  10:55 - 11:40", "12:40 - 13:25  13:30 - 14:15", "14:25 - 15:10  15:15 - 16:00", "16:10 - 16:55  17:00 - 17:45", "17:55 - 18:40  18:45 - 19:30"]
            if self.week_day == "Суббота":
                return ["8:15 - 9:40",  "9:50 - 11:20", "11:40 - 13:10", "13:20 - 14:50"]
            else: 
                return ["8:15 - 9:00  9:00 - 9:45", "10:05 - 10:50  10:55 - 11:40", "12:15 - 13:00  13:05 - 13:50", "14:00 - 14:45  14:50 - 15:35", "15:45 - 16:30  16:35 - 17:20", "17:30 - 18:15  18:20 - 19:05", "19:15 - 20:00  20:05 - 20:50"] 
        else:
            return self.__timing
    @timing.setter
    def timing(self, value):
        raise NameError("Только чтение")    

class Group():
    def __init__(self, name:str):
            self.__name = name.replace(" ", "")

    def __eq__(self, other:"Group") -> bool:
        if isinstance(other, "Group"):
            for feild, value in  self.__dict__.items():
                if  other.__dict__[feild] != value:
                    return False
            return True
        return False
    def __ne__(self, other:"Group")-> bool:
        return not self.__eq__(other)
    @property
    def name(self)->str:
        return self.__name
    @name.setter
    def name(self, value):
        raise NameError("Только чтение")
    @property
    def course(self)->str:
        return self.name[0]
    @course.setter
    def course(self, value):
        raise NameError("Только чтение")
    @property
    def spec(self)->str:
        return self.name[3]
    @spec.setter
    def spec(self, value):
        raise NameError("Только чтение")
    @property
    def sub_group(self)->str:
        return self.name[2]
    @sub_group.setter
    def sub_group(self, value):
        raise NameError("Только чтение")
    @property
    def school_year(self)->int:
        return self.name[4:]
    @school_year.setter
    def school_year(self, value):
        raise NameError("Только чтение")

class Lesson():
    def __init__(self, lesson: Dict[str,Any] = None, group:str = ""):
        if lesson:
            self.__para = lesson.get("index")
            self.__discipline = lesson.get("discipline")
            self.__group = group
            self.__cabs = self.split_cabs_row(lesson.get("classroom_raw", ""))

    def __str__(self):
        s = f"Пара №{self.para} по дисциплине {self.discipline} в кабинете {self.cabs} у группы {self.group}\n"
        return s

    def __eq__(self, other:"Lesson") -> bool:
        #if isinstance(other, "Lesson"):
            for feild, value in  self.__dict__.items():
                if  other.__dict__[feild] != value:
                    return False
            return True
        #return False
    def __ne__(self, other:Group)-> bool:
        return not self.__eq__(other)
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
             return [rooms]
    @property
    def discipline(self)->str:
        return self.__discipline
    @discipline.setter
    def discipline (self, value):
        raise NameError("Только чтение")
    @property
    def para(self)->int:
        return self.__para
    @para.setter
    def para(self, value):
        raise NameError("Только чтение")
    @property
    def group (self)->str:
        return self.__group
    @group.setter
    def group(self, value):
        raise NameError("Только чтение")
    @property
    def cabs(self)->List[str]:
        return self.__cabs
    @cabs.setter
    def cabs(self, value):
        raise NameError("Только чтение")
    @property
    def floors(cabs:list[str]) -> list[str]:
        resp = []
        for i in cabs:
            if i.isdecimal():
                if i[0] == "0":
                    resp.append("Подвал") 
                elif i[0] == ("1"):
                    resp.append("1 этаж") 
                elif i[0] == ("2"):
                    resp.append("2 этаж") 
                elif i[0] == ("3"):
                    resp.append("3 этаж") 
                elif i[0] == ("4"):
                    resp.append("4 этаж")
                elif i[0] == (""):
                    resp.append("Спортзал")
        return tuple(resp)