import asyncio
from aiogram import Bot, Dispatcher, Router, types, F, BaseMiddleware
from aiogram.filters import  Command
from aiogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button, Message, TelegramObject

        
bot = Bot(token="8597992462:AAHguxk307-4sBK1JYGnBGCT_rn_lPgz1Lg")
dp = Dispatcher()

from handlers.users import teacher_router, user_router

dp.message()

#включение роутера пользователей должно быть последним
dp.include_routers(teacher_router,user_router)

asyncio.run(dp.start_polling(bot))
