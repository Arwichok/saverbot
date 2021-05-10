from aiogram.types import Message, ContentType


def get_file_id(msg: Message):
    if msg.photo:
        file_id = msg.photo[-1].file_id
    else:
        file_id = {
            ContentType.ANIMATION: msg.animation,
            ContentType.AUDIO: msg.audio,
            ContentType.DOCUMENT: msg.document,
            ContentType.STICKER: msg.sticker,
            ContentType.VIDEO: msg.video,
            ContentType.VOICE: msg.voice,
        }.get(msg.content_type).file_id
    return file_id
