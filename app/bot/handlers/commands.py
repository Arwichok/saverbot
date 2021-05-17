from aiogram import Dispatcher, md
from aiogram.dispatcher.filters import CommandStart, CommandSettings, CommandHelp
import aiogram.types as atp
from sqlalchemy import select, delete, and_, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from app.bot.utils.markups import settings_markup
from app.bot.utils.messages import get_file_id, send_auto_delete, get_text
from app.models.message import Message
from app.models.user import User
from app.utils import config


async def welcome(msg: atp.Message):
    await msg.answer("Welcome to saver bot.\n"
                     "I save all your messages that you send me.\n"
                     "Share messages with inline mode.\n\n"
                     "Types: *g*if, *a*udio, *d*ocuments, *s*ticker, "
                     "*p*hoto, *t*ext, *vo*ice",
                     parse_mode="markdown")


async def users(msg: atp.Message, session: AsyncSession):
    users_list = await session.execute(select(User))
    users_list = users_list.scalars().all()
    await msg.answer("Users list\n" + "\n".join([
        md.hlink(user.name, f"tg://user?id={user.id}") for user in users_list
    ]))


async def settings(msg: atp.Message):
    await msg.answer("Settings", reply_markup=settings_markup())


async def help_cmd(msg: atp.Message):
    await msg.answer("Help page")


async def clear_cmd(msg: atp.Message, session: AsyncSession):
    r_msg = msg.reply_to_message
    cursor = await session.execute(update(Message).where(
        Message.uid == r_msg.from_user.id,
        or_(Message.file_id == get_file_id(msg), Message.text == get_text(msg)),
    ).values(text=""))
    if cursor.rowcount:
        await session.commit()
        await send_auto_delete(msg, "Cleared")


async def delete_cmd(msg: atp.Message, session: AsyncSession):
    r_msg = msg.reply_to_message
    cursor = await session.execute(delete(Message).where(
        Message.uid == r_msg.from_user.id,
        or_(Message.text == get_text(r_msg), Message.file_id == get_file_id(r_msg))
    ))
    if cursor.rowcount:
        await session.commit()
        await send_auto_delete(msg, "Deleted")


async def delete_all(msg: atp.Message, session: AsyncSession):
    await session.execute(delete(Message).where(Message.uid == msg.from_user.id))
    await session.commit()


async def not_replied(msg: atp.Message):
    await send_auto_delete(msg, "Not found message")


def register(dp: Dispatcher):
    dp.register_message_handler(welcome, CommandStart())
    dp.register_message_handler(settings, CommandSettings())
    dp.register_message_handler(help_cmd, CommandHelp())

    dp.register_message_handler(clear_cmd, commands="clear", is_reply=True)
    dp.register_message_handler(delete_cmd, commands="del", is_reply=True)
    dp.register_message_handler(not_replied, commands=["del", "clear"])
    dp.register_message_handler(delete_all, commands="delete_all")

    dp.register_message_handler(users, commands="users", user_id=config.OWNER_ID)
