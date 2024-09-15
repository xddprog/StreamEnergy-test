from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from lexicon.texts import menu_text
from keyboards.menu_keyboard import get_menu_keyboard


router = Router()


@router.message(CommandStart())
async def menu(message: Message, state: FSMContext):
    await message.answer(
        text=menu_text,
        reply_markup=await get_menu_keyboard(),
    )


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text=menu_text,
        reply_markup=await get_menu_keyboard(),
    )
