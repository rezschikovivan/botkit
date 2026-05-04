from aiogram.filters import  BaseFilter 
from aiogram.types import InlineKeyboardMarkup as Markup, InlineKeyboardButton as Button, Message, TelegramObject
from typing import List
from DB import User, Roles, UserRole, get_or_create_user

class CheckStatus(BaseFilter):
    def __init__(self, *allowed_roles: List[Roles]):
        self.allowed = allowed_roles
        
    async def __call__(self, msg: Message)->bool:
        user: User = get_or_create_user(msg.from_user.id)
        us_role = UserRole.get(UserRole.user == user).role
        #проверить роль
        for allowed in self.allowed:
            if allowed.name == us_role.name:
                return True
        return False
