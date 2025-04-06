from aiogram.fsm.state import State, StatesGroup

class AnonMessage(StatesGroup):
    sending_message = State()
    replying = State()
    chatting = State()  # Новое состояние для анонимного чата
