from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.bot.utils.constants import CONTENT_TYPES, DEF_TYPE, AVAILABLE_LANGUAGES, SET_LANG

DefaultType = CallbackData("ct", "c_type")
LanguageCD = CallbackData("lang", "lang")


def ct_button(title: str, c_type):
    return InlineKeyboardButton(title, callback_data=DefaultType.new(c_type))


def settings_markup(_, lang=None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(_("Default type", locale=lang), callback_data=DEF_TYPE)],
        [InlineKeyboardButton(_("Language", locale=lang), callback_data=SET_LANG)],
    ])


def content_types_markup(c_type):
    keys = []
    for key, val in CONTENT_TYPES.items():
        title = val.capitalize()
        keys.append([
            ct_button(f"[ {title} ]" if val == c_type else title, key)
        ])
    return InlineKeyboardMarkup(inline_keyboard=keys)


def language_markup(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(f"[{value}]" if lang == key else value, callback_data=LanguageCD.new(key))]
        for key, value in AVAILABLE_LANGUAGES.items()
    ])
