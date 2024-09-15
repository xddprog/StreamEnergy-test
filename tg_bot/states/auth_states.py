from aiogram.fsm.state import State, StatesGroup

class AuthStates(StatesGroup):
    is_not_auth = State()