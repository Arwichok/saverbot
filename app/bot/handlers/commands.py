from aiogram import Dispatcher, Bot, md
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import BotCommand
import aiogram.types as atp
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.markups.settings import settings_markup
from app.models.message import Message
from app.models.user import User


async def welcome(msg: atp.Message):
    await msg.answer("Hello, welcome to saver bot.\n"
                     "I save all your messages that you send me.\n"
                     "Share messages with inline mode.")


async def users(msg: atp.Message, session: AsyncSession):
    users_list = await session.execute(select(User))
    users_list = users_list.scalars().all()
    await msg.answer("Users list\n" + "\n".join([
        md.hlink(user.name, f"tg://user?id={user.id}") for user in users_list
    ]))


async def settings(msg: atp.Message):
    await msg.answer(
        "Settings", reply_markup=settings_markup()
    )


async def delete_cmd(msg: atp.Message, session: AsyncSession):
    reply_msg = msg.reply_to_message
    await session.execute(delete(Message).where(and_(
        Message.mid == reply_msg.message_id,
        Message.uid == msg.from_user.id,
    )))
    await session.commit()


async def delete_all(msg: atp.Message, session: AsyncSession):
    await session.execute(delete(Message).where(
        Message.uid == msg.from_user.id))
    await session.commit()


def register(dp: Dispatcher):
    dp.register_message_handler(welcome, CommandStart())
    dp.register_message_handler(users, commands="users", user_id=329398814)
    dp.register_message_handler(settings, commands="settings")
    dp.register_message_handler(delete_cmd, commands="del", is_reply=True)
    dp.register_message_handler(delete_all, commands="delete_all")


async def set_my_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand("start", "Start"),
        BotCommand("settings", "Settings"),
        BotCommand("del", "Delete message(Reply to original)"),
        BotCommand("delete_all", "Delete all messages"),
    ])
