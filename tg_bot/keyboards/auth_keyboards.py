from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.buttons import auth_buttons


async def get_auth_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in auth_buttons.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
