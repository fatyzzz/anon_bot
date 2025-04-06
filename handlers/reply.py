from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from states import AnonMessage
from db import get_message_sender
from config import logger

router = Router()

@router.callback_query(F.data == "reply")
async def reply_to_anon(callback: CallbackQuery, state: FSMContext) -> None:
    message_id = callback.message.message_id
    chat_id = callback.message.chat.id
    sender_chat_id = await get_message_sender(message_id, chat_id)
    if sender_chat_id:
        await state.update_data(reply_to=sender_chat_id)
        await state.set_state(AnonMessage.replying)
        await callback.message.answer("✍️ Напишите ваше ответное сообщение.")
    else:
        await callback.message.answer("❌ Не удалось найти отправителя.")
    await callback.answer()

@router.message(AnonMessage.replying)
async def send_reply(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    reply_to = data.get("reply_to")
    if reply_to:
        await message.bot.send_message(reply_to, f"✉️ <b>Ответ на ваше анонимное сообщение:</b>\n\n{message.text}", parse_mode="HTML")
        await message.answer("✅ Ответ отправлен анонимно.")
        logger.info(f"Reply sent from {message.chat.id} to {reply_to}")
    else:
        await message.answer("❌ Ошибка: не удалось отправить ответ.")
    await state.clear()