from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.utils.markups import content_types_markup, DefaultType, \
    settings_markup, LanguageCD, language_markup
from app.models.user import User
from app.bot.utils.constants import CONTENT_TYPES, DEF_TYPE, SET_LANG, AVAILABLE_LANGUAGES


async def default_type_page(cb: CallbackQuery, db_user: User):
    await cb.message.edit_reply_markup(content_types_markup(db_user.default_type))


async def content_type_callback(cb: CallbackQuery, session: AsyncSession, callback_data: dict, _):
    content_type = CONTENT_TYPES[callback_data.get("c_type")]
    await session.execute(update(User).where(User.id == cb.from_user.id).values(default_type=content_type))
    await session.commit()
    await cb.answer(_("Changed to {c_type}").format(c_type=content_type.capitalize()))
    await cb.message.edit_reply_markup(settings_markup(_))


async def language_callback(cb: CallbackQuery, session: AsyncSession, callback_data: dict, db_user, _):
    lang = callback_data.get("lang")
    db_user.language = lang
    await session.commit()
    await cb.answer(AVAILABLE_LANGUAGES.get(lang, "Default"))
    await cb.message.edit_text(_("Settings", locale=lang), reply_markup=settings_markup(_, lang))


async def set_lang_callback(cb: CallbackQuery, db_user, _):
    await cb.message.edit_reply_markup(language_markup(db_user.language))


def register(dp: Dispatcher):
    dp.register_callback_query_handler(default_type_page, text=DEF_TYPE)
    dp.register_callback_query_handler(set_lang_callback, text=SET_LANG)
    dp.register_callback_query_handler(language_callback, LanguageCD.filter())
    dp.register_callback_query_handler(content_type_callback, DefaultType.filter())
