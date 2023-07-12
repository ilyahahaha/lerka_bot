from aiogram.fsm.state import State, StatesGroup


class MainStateGroup(StatesGroup):
    results = State()
    loading = State()
    error = State()
