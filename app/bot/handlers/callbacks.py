from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.utils.markups import content_types_markup, DefaultType, \
    settings_markup
from app.models.user import User
from app.bot.utils.constants import CONTENT_TYPES, DEF_TYPE


async def default_type_page(cb: CallbackQuery, db_user: User):
    await cb.message.edit_reply_markup(content_types_markup(db_user.default_type))


async def content_type_callback(cb: CallbackQuery, session: AsyncSession, callback_data: dict):
    content_type = CONTENT_TYPES[callback_data.get("c_type")]
    await session.execute(update(User).where(User.id == cb.from_user.id).values(default_type=content_type))
    await session.commit()
    await cb.answer(f"Changed to {content_type.capitalize()}")
    await cb.message.edit_reply_markup(settings_markup())


def register(dp: Dispatcher):
    dp.register_callback_query_handler(default_type_page, text=DEF_TYPE)
    dp.register_callback_query_handler(content_type_callback, DefaultType.filter())
