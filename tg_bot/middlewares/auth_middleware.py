from email import header
from urllib import response
import requests_async as req

from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram import BaseMiddleware, Dispatcher
from aiogram.types import Update, TelegramObject
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from states.auth_states import AuthStates



class AuthCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        state: FSMContext = data.get('state')

        if state.get('token'):
            response = await req.get(
                'https://localhost:8000/api/auth/current_user', 
                headers={'Authorization': f'Bearer {data['state'].get('token')}'}
            )
            if response.status_code == 200:
                data['is_login'] = True
        else:
            data['is_login'] = False
            state.set_state(AuthStates.is_not_auth)
        
        return await handler(event, data)

