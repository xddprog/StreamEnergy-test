from aiogram import Router
from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.auth_states import AuthStates
from filters.auth_filter import AuthFilter


router = Router()


@router.message(AuthFilter())
async def user_unauthorized(message: Message, state: FSMContext) -> None:
    
    await message.reply("Вы не авторизованы")

