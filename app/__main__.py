from aiogram import executor, Dispatcher

from app.bot.dp import init_dp, init_bot
from app.bot.handlers import commands, messages, inlines, callbacks
from app.bot.middlewares.db import DBMiddleware
from app.models.db import init_session
from app.utils import config
from app.utils.logging import init_log


async def on_startup(dp: Dispatcher):
    inlines.register(dp)
    commands.register(dp)
    messages.register(dp)
    callbacks.register(dp)
    await commands.set_my_commands(dp.bot)
    session = await init_session(config.DB_URL)
    dp.setup_middleware(DBMiddleware(session))


def main():
    init_log()
    executor.start_polling(
        dispatcher=init_dp(init_bot(config.BOT_TOKEN)),
        on_startup=on_startup,
        skip_updates=True
    )


if __name__ == '__main__':
    main()
