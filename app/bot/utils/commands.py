from aiogram import Bot
from aiogram.types import BotCommand


async def set_my_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand("start", "Start"),
        BotCommand("settings", "Settings"),
        BotCommand("clear", "Clear caption (Reply to original)"),
        BotCommand("del", "Delete message (Reply to original)"),
        BotCommand("delete_all", "Delete all messages"),
    ])
