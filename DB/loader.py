import json
import os
import enum
from peewee import *
    
my_id = 5328981727

dir_path = os.path.dirname(os.path.abspath(__file__))


def download(name:str,value_to_read):#загрузить
        with open(dir_path + rf"\{name}", "r") as f:
            # Записываем словарь
            value_to_read = json.load(f)
        print(f"Дынные десереализованы в {value_to_read}")
        return value_to_read

def upload(name:str,value_to_write):#выгрузить
        with open(dir_path + rf"\{name}", "w") as f:
            #записываем в файл
            json.dump(value_to_write, f,)
        print("Данные сереализованы")

db = SqliteDatabase("users.db")

class Table(Model):

    class Meta:
        database = db

class User(Table):
    tg_id = IntegerField(unique=True, primary_key= True)

class Role(Table):
    name = CharField()

class UserRole(Table):
    user = ForeignKeyField(User)
    role = ForeignKeyField(Role)

class Permition(Table):
    permition = CharField()

class RolePermition(Table):
    role = ForeignKeyField(Role)
    permition = ForeignKeyField(Permition)

class Teacher(Table):
    user = ForeignKeyField(User)

class Dispatch(Table):
    user = ForeignKeyField(User)

class Technic(Table):
    user = ForeignKeyField(User)
    get_notifications = BooleanField(default=False)


#Задаем все роли
Roles = enum.Enum("Roles", names=[
    "Polzovatel",
    "Teacher",
    "Dispatcher",
    "Technic"
    ],)

def get_or_create_user(us_id:int, new_role:Roles = Roles.Polzovatel):
    user, created = User.get_or_create(tg_id=us_id)    
    if created:
        UserRole.create(user_id=user.tg_id, role_id=Role.get(name=new_role.name))
    return user

def set_role(us_id:int, new_role: Roles):
    user = get_or_create_user(us_id=us_id)
    us_role = UserRole.get(user_id=user.tg_id)
    us_role.role = Role.get(name=new_role.name)
    us_role.save()


if __name__ == '__main__':

    db.create_tables(models = [User, Role, Permition, Teacher, RolePermition, UserRole])

    for role in Roles:
        Role.get_or_create(name = role.name)

    #Задаем все команды
    permitions = ["Посмотреть всё расписание", "Посмотреть расписание на сегодня"]
    for perm in permitions:
        Permition.get_or_create(permition = perm)

    #Задаем команды для ролей
    rolepermitions = [
        ("Преподаватель", "Запросить кабинет"),
        ("Диспетчер", "Одобрить кабинет"),
        ("Диспетчер", "Отклонить кабинет"),
        ("Техник", "Получать уведомления об ошибках"),
        ("Техник", "Не получать уведомления об ошибках")
        ]
    for role, permition in rolepermitions:
        RolePermition.get_or_create(role = role, permition = permition)

    set_role(my_id, Roles.Teacher)
    ur = UserRole.get(UserRole.user == User.get(User.tg_id == my_id))
    print(ur.role.name)










