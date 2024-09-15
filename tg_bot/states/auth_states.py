from aiogram.fsm.state import State, StatesGroup


class CheckAuthState(StatesGroup):
    is_not_auth = State()


class AuthStates(StatesGroup):
    login = State()
    password = State()
