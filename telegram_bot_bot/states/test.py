from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import dp

class Test(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    feedback = State()
    admin_check = State()
    wait = State()
    payment_reciept = State()
    payment = State()
    balance_amount = State()
    top_up_balance = State()
    balance_history_count = State()


