from aiogram.types import ContentType


CONTENT_TYPES = dict(g=ContentType.ANIMATION, a=ContentType.AUDIO,
                     d=ContentType.DOCUMENT, p=ContentType.PHOTO,
                     s=ContentType.STICKER, t=ContentType.TEXT,
                     v=ContentType.VIDEO, vo=ContentType.VOICE)
DEF_TYPE = "def_type"
DB_USER = "db_user"
SESSION = "session"
