import requests_async as req

from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext

from states.auth_states import AuthStates


class AuthCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        state: FSMContext = data.get("state")
        state_data = await state.get_data()

        if data:
            response = await req.get(
                "http://localhost:8000/api/auth/current_user",
                headers={
                    "Authorization": f'Bearer {state_data.get('token')}'
                },
            )

            if response.status_code == 200:
                return await handler(event, data)
            
        await state.set_state(AuthStates.is_not_auth)
        data['state'] = state
        return await handler(event, data)
