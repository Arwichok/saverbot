import asyncio

from aiogram import Dispatcher, md
from aiogram.dispatcher.filters import CommandStart, CommandSettings, CommandHelp
import aiogram.types as atp
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.utils.markups import settings_markup
from app.bot.utils.messages import get_file, send_auto_delete
from app.models.message import Message
from app.models.user import User
from app.utils import config


async def welcome(msg: atp.Message, _):
    await msg.answer(_("Welcome message"))


async def users(msg: atp.Message, session: AsyncSession):
    users_list = (await session.execute(select(User))).scalars().all()
    await msg.answer("Users list\n" + "\n".join([
        md.hlink(user.name, f"tg://user?id={user.id}") for user in users_list
    ]))


async def settings(msg: atp.Message, _):
    await msg.answer(_("Settings"), reply_markup=settings_markup(_))


async def help_cmd(msg: atp.Message, _):
    await msg.answer(_("Help page"))


async def clear_cmd(msg: atp.Message, session: AsyncSession, _):
    r_msg = msg.reply_to_message
    if file := get_file(r_msg):
        cursor = await session.execute(update(Message).where(
            Message.uid == r_msg.from_user.id,
            Message.file_unique_id == file.file_unique_id,
        ).values(text=""))
        if cursor.rowcount:
            await session.commit()
            await send_auto_delete(msg, _("Cleared"))


async def delete_cmd(msg: atp.Message, session: AsyncSession, _):
    r_msg = msg.reply_to_message
    file = get_file(r_msg)
    file_uid = file.file_unique_id if file else ""
    cursor = await session.execute(delete(Message).where(
        Message.uid == r_msg.from_user.id,
        Message.file_unique_id == file_uid,
    ))
    if cursor.rowcount:
        await session.commit()
        await send_auto_delete(msg, _("Deleted"))


async def delete_all(msg: atp.Message, session: AsyncSession, _):
    await session.execute(delete(Message).where(Message.uid == msg.from_user.id))
    await session.commit()
    await send_auto_delete(msg, _("All messages deleted"))


async def not_replied(msg: atp.Message, _):
    await send_auto_delete(msg, _("Not found message"))


def register(dp: Dispatcher):
    dp.register_message_handler(welcome, CommandStart())
    dp.register_message_handler(settings, CommandSettings())
    dp.register_message_handler(help_cmd, CommandHelp())

    dp.register_message_handler(clear_cmd, commands="clear", is_reply=True)
    dp.register_message_handler(delete_cmd, commands="del", is_reply=True)
    dp.register_message_handler(not_replied, commands=["del", "clear"])
    dp.register_message_handler(delete_all, commands="delete_all")

    dp.register_message_handler(users, commands="users", user_id=config.OWNER_ID)
