from aiogram import Dispatcher
import aiogram.types as atp
from aiogram.types import ContentType as act
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.utils.bot import get_file_id
from app.utils.constants import CONTENT_TYPES


async def new_message(msg: atp.Message, session: AsyncSession):
    await msg.answer_chat_action("upload_document")
    text = file_id = ""
    if msg.content_type == act.TEXT:
        text = msg.text
    else:
        text = msg.caption
        if msg.photo:
            file_id = msg.photo[-1].file_id
        elif msg.audio and not msg.audio.title:
            await msg.answer("I can't save Audio without Title")
            return
        else:
            file_id = {
                act.ANIMATION: msg.animation,
                act.DOCUMENT: msg.document,
                act.AUDIO: msg.audio,
                act.STICKER: msg.sticker,
                act.VIDEO: msg.video,
                act.VOICE: msg.voice,
            }.get(msg.content_type).file_id
    session.add(Message(
        mid=msg.message_id,
        uid=msg.from_user.id,
        type=msg.content_type,
        text=text,
        file_id=file_id,
    ))
    await session.commit()


async def via_bot_filter(msg: atp.Message):
    if msg.via_bot:
        return msg.via_bot.id != msg.bot.id
    return True


async def edit_message(msg: atp.Message, session: AsyncSession):
    if msg.content_type == act.TEXT:
        await session.execute(update(Message).where(
            Message.mid == msg.message_id,
            Message.uid == msg.from_user.id,
        ).values(text=msg.text))
    else:
        file_id = get_file_id(msg)
        await session.execute(update(Message).where(
            Message.mid == msg.message_id,
            Message.uid == msg.from_user.id,
        ).values(text=msg.caption, file_id=file_id))
    await session.commit()


def register(dp: Dispatcher):
    dp.register_message_handler(
        new_message,
        via_bot_filter,
        chat_type=atp.ChatType.PRIVATE,
        content_types=CONTENT_TYPES.values(),
    )
    dp.register_edited_message_handler(
        edit_message,
        chat_type=atp.ChatType.PRIVATE,
        content_types=CONTENT_TYPES.values(),
    )
