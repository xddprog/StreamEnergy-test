from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from lexicon.buttons import menu_buttons


async def get_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=key)]
        for key, value in menu_buttons.items()
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
