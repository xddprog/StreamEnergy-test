import requests as req

from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext

from states.auth_states import CheckAuthState


class AuthCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        state: FSMContext = data.get("state")
        state_data = await state.get_data()

        if state_data.get("auth_type"):
            return await handler(event, data)

        if data:
            response = req.get(
                "http://app:8000/api/auth/current_user",
                headers={"Authorization": f'Bearer {state_data.get('token')}'},
            )

            if response.status_code == 200:
                return await handler(event, data)

        await state.set_state(CheckAuthState.is_not_auth)
        data["state"] = state
        return await handler(event, data)
