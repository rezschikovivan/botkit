from aiogram import Bot, Dispatcher, Router, types, F, BaseMiddleware
from aiogram.filters import  Command
from aiogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button, Message, TelegramObject
from DB import Roles, set_role

from DB import CheckStatus


teacher_router = Router()
teacher_router.message.filter(CheckStatus(Roles.Technic, Roles.Teacher))

@teacher_router.message(Command("start"))
async def hello(msg: Message):
    await msg.answer("ты преподователь")
    set_role(msg.from_user.id, Roles.Polzovatel)

user_router = Router()

@user_router.message(Command("start"))
async def hi(msg:Message):
    await msg.answer(str("ты пользователь"))
    set_role(msg.from_user.id, Roles.Teacher)