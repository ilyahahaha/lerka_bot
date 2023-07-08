from aiogram.fsm.state import State, StatesGroup


class MainStateGroup(StatesGroup):
    default = State()
    results = State()
    loading = State() 
