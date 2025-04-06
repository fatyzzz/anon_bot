from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_reply_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✉️ Ответить", callback_data="reply")]
    ])