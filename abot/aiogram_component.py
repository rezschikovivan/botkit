from abot.core import BaseComponent, BaseFilterImplementor, BaseMsg
from abot.message import BaseMsg, Sender, Keyboard
from typing import Dict
from aiogram.types import Message, KeyboardButton, InlineKeyboardButton 
from aiogram.filters import BaseFilter
from aiogram import Bot, Dispatcher

#компонент должен реализовать абстрактный класс, проверить с помощю: AiogramFilter()
class AiogramFilter(BaseFilterImplementor):
    def func(self, f: callable):
        class CustomFilter(BaseFilter):
            def __init__(self, *func: callable):
                self.func = func

            def __call__(self, event)->bool:
                for f in self.func:
                    if f(event): continue
                    return False
                else: return True
        return CustomFilter(f)
    
#компонент должен реализовать абстрактный класс, проверить с помощю: AiogramMsg()
class AiogramMsg(BaseMsg):
    msg: Message
    def __init__(self, msg: Message):
        super().__init__(msg)
    @classmethod
    def msg_type(cls):
        return Message
    async def answer(self, text: str):
        return await self.msg.answer(text)
    
    async def reply(self, text: str) -> Message:
        return await self.msg.reply(text)
    
    async def delete(self):
        return await self.msg.delete()
    
    
    async def send_reply_kboard(self, keyboard:Keyboard, text:str|None = None):
        ai_keyboard:Keyboard = Keyboard(True, False)
        self.create_ai_kboard(ai_keyboard, keyboard)
        await self.msg.answer(text, keyboard=ai_keyboard)

    def create_ai_kboard(self, keyboard: Keyboard) -> list[list[KeyboardButton]]:
        row = []
        current_row = []
        current_row_index = 0 

        for button in keyboard.buttons:
            if button.row != current_row_index:
                if current_row:
                    row.append(current_row)
                current_row = []
                current_row_index = button.row
            current_row.append(KeyboardButton(text=button.text))
        if current_row:
            row.append(current_row)
        return row

    async def send_inline_kboard(self, keyboard:Keyboard, text:str|None = None):
        ai_keyboard:Keyboard = Keyboard(False, True)
        self.create_ai_kboard(ai_keyboard, keyboard)
        await self.msg.answer(text, keyboard=ai_keyboard)
    
    def create_inline_kboard(self, keyboard: Keyboard) -> list[list[InlineKeyboardButton]]:
        row = []
        current_row = []
        current_row_index = 0
    
        for button in keyboard.buttons:
            if button.row != current_row_index:
                if current_row:
                    row.append(current_row)
                current_row = []
                current_row_index = button.row

            if button.is_url:
                inline_button = InlineKeyboardButton(
                    text=button.text,
                    url=button.action
                )
            elif button.is_callback:
                inline_button = InlineKeyboardButton(
                    text=button.text,
                    callback_data=str(list(button.action.values())[0])
                )
            else:
                inline_button = InlineKeyboardButton(
                    text=button.text,
                    callback_data=str(button.action) if button.action else button.text
                )
            current_row.append(inline_button)
        if current_row:
            row.append(current_row)
        return row


    @property
    def date(self):
        return self.msg.date
    
    @property
    def text(self):
        return self.msg.text or ""
    
    @property
    def photo(self):
        return self.msg.photo[-1] if self.msg.photo else None
    
    @property
    def document(self):
        return self.msg.document
    
    @property
    def audio(self):
        return self.msg.audio
    
    @property
    def video(self):
        return self.msg.video
    
    @property
    def location(self):
        return self.msg.location
    
    @property
    def voice(self):
        return self.msg.voice
    
    @property
    async def sender(self):
        user = self.msg.from_user
        if user:
            return None

#компонент должен реализовать абстрактный класс
class AiogramComponent(BaseComponent):
    bots: Dict[str,Bot] = {}
    dispatchers: Dict[str,Dispatcher] = {}
    @classmethod
    def get_filter(cls):
        return AiogramFilter
    @classmethod
    def get_messager(cls):
        pass
    @classmethod
    def add_bot(cls, token:str):
        if not token in cls.bots.keys():
            cls.bots[token] = Bot(token=token)
            cls.dispatchers[token] = Dispatcher()
    @classmethod
    def register_handler(cls, token, method, *filters):
        cls.dispatchers[token].message.register(method, *filters)
    @classmethod
    def cretae_polling_tasks(cls):
        tasks = []
        for token, disp in cls.dispatchers.items():
            tasks.append(disp.start_polling(cls.bots[token]))
        return tasks
