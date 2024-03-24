from aiogram.fsm.state import State, StatesGroup

class WandererCreateForm(StatesGroup):
    title = State()
    desc = State()
    url = State()
    photo = State()