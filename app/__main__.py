from aiogram import executor, Dispatcher

from app.bot.dp import init_dp, init_bot
from app.bot.handlers import commands, messages, inlines, callbacks
from app.bot.middlewares.acl import ACLMiddleware
from app.bot.middlewares.db import DBMiddleware
from app.bot.utils.commands import set_my_commands
from app.models.db import init_session, init_engine, setup_models
from app.utils import config
from app.utils.logging import init_log


async def on_startup(dp: Dispatcher):
    callbacks.register(dp)
    commands.register(dp)
    inlines.register(dp)
    messages.register(dp)

    await set_my_commands(dp.bot)
    engine = init_engine()
    await setup_models(engine)
    session = init_session(engine)

    dp.setup_middleware(DBMiddleware(session))
    dp.setup_middleware(ACLMiddleware())


def main():
    init_log()
    executor.start_polling(
        dispatcher=init_dp(init_bot(config.BOT_TOKEN)),
        on_startup=on_startup,
        skip_updates=True
    )


if __name__ == '__main__':
    main()
