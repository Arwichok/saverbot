from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message, CallbackQuery, InlineQuery

from app.bot.utils.constants import DB_USER, SESSION
from app.models.user import User


class ACLMiddleware(LifetimeControllerMiddleware):
    def __init__(self):
        super().__init__()
        self.skip_patterns = ["update"]

    async def pre_process(self, obj, data, *args):
        if isinstance(obj, (Message, CallbackQuery, InlineQuery)) and obj:
            data[DB_USER] = await User.create(data[SESSION], obj.from_user)
