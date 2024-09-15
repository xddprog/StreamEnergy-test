from aiogram.fsm.state import State, StatesGroup


class CreateTask(StatesGroup):
    title = State()
    description = State()
    tags = State()
