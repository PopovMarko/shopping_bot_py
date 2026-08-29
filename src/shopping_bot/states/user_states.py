from aiogram.fsm.state import State, StatesGroup


class WaitFor(StatesGroup):
    product = State()
    quantity = State()
    confirmation = State()
    unit = State()
