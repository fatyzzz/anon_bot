from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from states.anon_message import AnonMessage
from db.redis_db import get_chat_id, get_chat_owner
from config import logger

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    logger.info(f"Start command from {message.chat.id} with text: {message.text}")
    if len(message.text.split()) > 1:
        unique_code = message.text.split()[1]
        chat_id = await get_chat_id(unique_code)  # Основная ссылка
        owner_chat_id = await get_chat_owner(unique_code)  # Чат-ссылка
        target_chat_id = owner_chat_id or chat_id
        if target_chat_id:
            await state.update_data(unique_code=unique_code, target_chat_id=target_chat_id)
            await state.set_state(AnonMessage.sending_message)
            current_state = await state.get_state()
            logger.info(f"User {message.chat.id} started sending to {target_chat_id} with code {unique_code}, state: {current_state}")
            await message.answer("✍️ Напишите сообщение, которое будет отправлено анонимно.")
        else:
            await message.answer("❌ Неверный код.")
            logger.warning(f"Invalid code {unique_code} from {message.chat.id}")
    else:
        await message.answer(
            "<b>👋 Привет!</b>\n\n"
            "Я бот для анонимных сообщений. Используйте команды:\n"
            "- /getlink — получить уникальную ссылку\n"
            "- /chat — начать анонимный чат\n"
            "- /help — справка",
            parse_mode="HTML"
        )