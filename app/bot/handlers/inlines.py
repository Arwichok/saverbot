from aiogram import Dispatcher
from aiogram.types import InlineQuery, ContentType, InlineQueryResultArticle, \
    InputTextMessageContent, InlineQueryResultCachedPhoto, \
    InlineQueryResultCachedGif, InlineQueryResultCachedAudio, \
    InlineQueryResultCachedDocument, InlineQueryResultCachedSticker, \
    InlineQueryResultCachedVideo, InlineQueryResultCachedVoice
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Message
from app.models.user import User
from app.utils.constants import CONTENT_TYPES


async def search(iq: InlineQuery, session: AsyncSession, db_user: User):
    # Get content type by query or user default type
    content_type = CONTENT_TYPES.get(iq.query, db_user.default_type)
    # Get messages by content type
    msgs = (await session.execute(
        select(Message).where(
            Message.uid == iq.from_user.id,
            Message.type == content_type
        )
    )).scalars().all()
    # Write to `results` list of results by content type
    results = get_results(content_type, msgs)
    await iq.answer(results, cache_time=1)


def get_results(content_type: str, msgs):
    return [{
        ContentType.ANIMATION: get_gif_result,
        ContentType.AUDIO: get_audio_result,
        ContentType.DOCUMENT: get_document_result,
        ContentType.PHOTO: get_photo_result,
        ContentType.STICKER: get_sticker_result,
        ContentType.TEXT: get_text_result,
        ContentType.VIDEO: get_video_result,
        ContentType.VOICE: get_voice_result,
    }.get(content_type)(msg) for msg in msgs]


def get_gif_result(msg: Message):
    return InlineQueryResultCachedGif(
        id=msg.rowid, caption=msg.text, gif_file_id=msg.file_id
    )


def get_audio_result(msg: Message):
    return InlineQueryResultCachedAudio(
        id=msg.rowid, caption=msg.text, audio_file_id=msg.file_id
    )


def get_document_result(msg: Message):
    return InlineQueryResultCachedDocument(
        id=msg.rowid,
        title=msg.text,
        document_file_id=msg.file_id,
        caption=msg.text
    )


def get_photo_result(msg: Message):
    return InlineQueryResultCachedPhoto(
        id=msg.rowid, caption=msg.text, photo_file_id=msg.file_id,
    )


def get_sticker_result(msg: Message):
    return InlineQueryResultCachedSticker(
        id=msg.rowid, sticker_file_id=msg.file_id
    )


def get_text_result(msg: Message):
    return InlineQueryResultArticle(
        id=msg.rowid,
        title=msg.text,
        input_message_content=InputTextMessageContent(msg.text)
    )


def get_video_result(msg: Message):
    return InlineQueryResultCachedVideo(
        id=msg.rowid,
        title=msg.text,
        caption=msg.text,
        video_file_id=msg.file_id
    )


def get_voice_result(msg: Message):
    return InlineQueryResultCachedVoice(
        id=msg.rowid,
        title=msg.text,
        caption=msg.text,
        voice_file_id=msg.file_id
    )


def register(dp: Dispatcher):
    dp.register_inline_handler(search)
