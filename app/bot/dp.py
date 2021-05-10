from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage


def init_bot(token: str) -> Bot:
    return Bot(
        token=token,
        parse_mode="html"
    )


def init_dp(bot: Bot) -> Dispatcher:
    storage = MemoryStorage()
    return Dispatcher(bot, storage=storage)
