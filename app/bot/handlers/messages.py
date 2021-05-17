from aiogram import Dispatcher
import aiogram.types as atp
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.bot.utils.messages import get_file_id, send_auto_delete, get_text
from app.bot.utils.constants import CONTENT_TYPES


async def new_message(msg: atp.Message, session: AsyncSession):
    session.add(Message(
        mid=msg.message_id,
        uid=msg.from_user.id,
        type=msg.content_type,
        text=get_text(msg),
        file_id=get_file_id(msg),
    ))
    await session.commit()
    await send_auto_delete(msg, "Saved")


async def edit_message(msg: atp.Message, session: AsyncSession):
    out = await session.execute(update(Message).where(
        Message.uid == msg.from_user.id,
        Message.mid == msg.message_id,
    ).values(
        text=get_text(msg),
        file_id=get_file_id(msg)
    ))
    await session.commit()
    if out.rowcount:
        await msg.answer_chat_action(atp.ChatActions.TYPING)


async def message_filter(msg: atp.Message):
    if msg.via_bot and msg.via_bot.id == msg.bot.id:
        await send_auto_delete(msg, "I ignore my messages")
    elif msg.audio and not msg.audio.title:
        await send_auto_delete(msg, "I can't save audio without title")
    else:
        return True
    return False


def register(dp: Dispatcher):
    dp.register_message_handler(
        new_message,
        message_filter,
        chat_type=atp.ChatType.PRIVATE,
        content_types=CONTENT_TYPES.values(),
    )
    dp.register_edited_message_handler(
        edit_message,
        message_filter,
        chat_type=atp.ChatType.PRIVATE,
        content_types=CONTENT_TYPES.values(),
    )
