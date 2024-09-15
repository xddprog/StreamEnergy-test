import requests as req
from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from filters.auth_filter import AuthFilter
from keyboards.auth_keyboards import get_auth_keyboard
from lexicon.texts import auth_texts
from states.auth_states import AuthStates


router = Router()


async def login_user(login: str, password: str) -> None:
    response = req.post(
        "http://app:8000/api/auth/login",
        json={"login": login, "password": password},
    )

    if response.status_code == 200:
        return response.json()["token"]

    return response.json()


async def register_user(login: str, password: str) -> None:
    response = req.post(
        "http://app:8000/api/auth/register",
        json={"login": login, "password": password},
    )

    if response.status_code == 201:
        return response.json()["token"]

    return response.json()


async def auth_user(auth_type: str, login: str, password: str) -> None:
    if auth_type == "login":
        return await login_user(login, password)
    return await register_user(login, password)


@router.callback_query(F.data == "login")
async def login(callback: CallbackQuery, state: FSMContext):
    await state.update_data(auth_type="login")
    await state.set_state(AuthStates.login)

    await callback.message.edit_text(text=auth_texts["login"])


@router.callback_query(F.data == "register")
async def register(callback: CallbackQuery, state: FSMContext):
    await state.update_data(auth_type="register")
    await state.set_state(AuthStates.login)

    await callback.message.edit_text(text=auth_texts["login"])


@router.callback_query(F.data == "login")
async def login(callback: CallbackQuery, state: FSMContext):
    await state.update_data(auth_type="login")
    await state.set_state(AuthStates.login)

    await callback.message.edit_text(text=auth_texts["login"])


@router.message(AuthStates.login)
async def password(message: Message, state: FSMContext):
    await state.update_data(login=message.text)
    await state.set_state(AuthStates.password)

    await message.answer(text=auth_texts["password"])


@router.message(AuthStates.password)
async def check_auth(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    auth_result = await auth_user(**data)

    if isinstance(auth_result, str):
        await state.clear()

        await state.update_data(token=auth_result)

        if data["auth_type"] == "login":
            await message.answer(text=auth_texts["login_succesfull"])
        else:
            await message.answer(text=auth_texts["register_succesfull"])
    else:
        await message.answer(
            text=auth_result["detail"],
            reply_markup=await get_auth_keyboard(),
        )


@router.message(AuthFilter())
async def user_unauthorized(message: Message, state: FSMContext) -> None:
    await message.reply(
        text="Вы не авторизованы",
        reply_markup=await get_auth_keyboard(),
    )
    