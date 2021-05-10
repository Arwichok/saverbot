from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message, InlineQuery, CallbackQuery

from app.models.user import User

SESSION = "session"


class DBMiddleware(LifetimeControllerMiddleware):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.skip_patterns = ["update"]

    async def pre_process(self, obj, data, *args):
        session = self.session()
        await session.begin()
        data[SESSION] = session
        if isinstance(obj, (Message, InlineQuery, CallbackQuery)):
            data["db_user"] = await User.create(session, obj.from_user)

    async def post_process(self, obj, data, *args):
        if session := data[SESSION]:
            await session.close()
