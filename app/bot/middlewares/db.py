from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from app.bot.utils.constants import SESSION


class DBMiddleware(LifetimeControllerMiddleware):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.skip_patterns = ["update"]

    async def pre_process(self, obj, data, *args):
        session = self.session()
        assert isinstance(SESSION, str)
        data[SESSION] = session

    async def post_process(self, obj, data, *args):
        session = data.get(SESSION)
        if session:
            await session.close()
