from aiogram.types import InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from app.utils.constants import CONTENT_TYPES


CTypeData = CallbackData("ct", "c_type")


def ct_button(title: str, c_type):
    return InlineKeyboardButton(title, callback_data=CTypeData.new(c_type))


def settings_markup():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("Default type", callback_data="def_type")]]
    )


def content_types_markup(c_type):
    keys = []
    for key, val in CONTENT_TYPES.items():
        title = val.capitalize()
        keys.append([
            ct_button(f"[ {title} ]" if val == c_type else title, key)
        ])
    return InlineKeyboardMarkup(inline_keyboard=keys)
