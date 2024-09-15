from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.auth_states import CheckAuthState


class AuthFilter(BaseFilter):
    async def __call__(self, message: Message, state: FSMContext) -> bool:
        return await state.get_state() == CheckAuthState.is_not_auth
