from aiogram.types import ContentType, InlineQueryResultCachedGif, InlineQueryResultCachedAudio, \
    InlineQueryResultCachedDocument, InlineQueryResultCachedPhoto, InlineQueryResultCachedSticker, \
    InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultCachedVideo, InlineQueryResultCachedVoice, \
    InlineQueryResult

from app.models.message import Message


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
    print(msg.file_id, msg.text)
    return InlineQueryResultCachedAudio(
        id=msg.rowid,
        caption=msg.text,
        audio_file_id=msg.file_id,
    )


def get_document_result(msg: Message):
    return InlineQueryResultCachedDocument(
        id=msg.rowid,
        title=msg.text or "Document",
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
        title=msg.text or "Video",
        caption=msg.text,
        video_file_id=msg.file_id
    )


def get_voice_result(msg: Message):
    return InlineQueryResultCachedVoice(
        id=msg.rowid,
        title=msg.text or "Voice",
        caption=msg.text,
        voice_file_id=msg.file_id
    )
