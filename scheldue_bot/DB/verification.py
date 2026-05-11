﻿from abot import ABCMsger
from typing import List
from scheldue_bot.DB import User, Roles, UserRole, get_or_create_user

class CheckStatus():
    def __init__(self, *allowed_roles: List[Roles]):
        self.allowed = allowed_roles
        
    async def __call__(self, msg: ABCMsger)->bool:
        user: User = get_or_create_user(msg.sender.id)
        us_role = UserRole.get(UserRole.user == user).role
        #проверить роль
        for allowed in self.allowed:
            if allowed.name == us_role.name:
                return True
        return False
