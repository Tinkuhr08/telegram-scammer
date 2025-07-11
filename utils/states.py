# utils/states.py

from aiogram.fsm.state import State, StatesGroup

class ReportScammer(StatesGroup):
    telegram_id = State()
    upi_id = State()
    phone_number = State()
    image = State()
    proof = State()
    amount = State() 

class Appeal(StatesGroup):
    reason = State()
    proof = State()
