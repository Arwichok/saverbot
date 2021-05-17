import asyncio

from aiogram.types import ContentType as act, Message


def get_file_id(msg: Message):
    file = {
        act.ANIMATION: msg.animation,
        act.AUDIO: msg.audio,
        act.DOCUMENT: msg.document,
        act.STICKER: msg.sticker,
        act.VIDEO: msg.video,
        act.VOICE: msg.voice,
        act.PHOTO: msg.photo,
    }.get(msg.content_type)
    file = file[-1] if msg.photo else file
    return file.file_id if file else ""


async def send_auto_delete(msg: Message, text: str, delay: float = 10):
    out_msg = await msg.answer(text)
    await asyncio.sleep(delay)
    await out_msg.delete()
