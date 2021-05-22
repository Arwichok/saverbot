from aiogram import Dispatcher
import aiogram.types as atp
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.bot.utils.messages import get_file, send_auto_delete, get_text
from app.bot.utils.constants import CONTENT_TYPES


async def new_message(msg: atp.Message, session: AsyncSession, _, file_id, file_uid):
    db_msg = await session.execute(select(Message).where(
        Message.uid == msg.from_user.id, Message.file_unique_id == file_uid
    ))
    if db_msg.scalar():
        return await send_auto_delete(msg, _("Media exists"))
    session.add(Message(
        mid=msg.message_id,
        uid=msg.from_user.id, 
        type=msg.content_type,
        text=get_text(msg),
        file_id=file_id,
        file_unique_id=file_uid,
    ))
    await session.commit()
    await send_auto_delete(msg, _("Saved"))


async def edit_message(msg: atp.Message, session: AsyncSession, _, file_uid):
    out = await session.execute(update(Message).where(
        Message.uid == msg.from_user.id,
        Message.file_unique_id == file_uid,
    ).values(text=get_text(msg)))
    if out.rowcount:
        await session.commit()
        await msg.answer_chat_action(atp.ChatActions.TYPING)


async def message_filter(msg: atp.Message):
    _ = Dispatcher.get_current().get("i18n").gettext
    if msg.via_bot and msg.via_bot.id == msg.bot.id:
        await send_auto_delete(msg, _("I ignore my messages"))
    elif msg.audio and not msg.audio.title:
        await send_auto_delete(msg, _("I can't save audio without title field"))
    elif msg.video and msg.video.mime_type != "video/mp4":
        await send_auto_delete(msg, _("Video mime type not valid"))
    else:
        file = get_file(msg)
        return dict(
            file_id=file.file_id if file else "",
            file_uid=file.file_unique_id if file else "",
        )
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
