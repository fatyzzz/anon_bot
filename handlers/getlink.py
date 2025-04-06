from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from utils.helpers import generate_unique_code
from db.redis_db import save_link, redis_client
from config import BOT_USERNAME, logger

router = Router()

@router.message(Command("getlink"))
async def get_link(message: Message) -> None:
    chat_id = message.chat.id
    unique_code = await redis_client.get(f"chat:{chat_id}")  # Проверяем существующий код
    if not unique_code:
        unique_code = generate_unique_code()  # Создаём новый, если нет
        await save_link(unique_code, chat_id)
        logger.info(f"Generated new link for chat {chat_id}: {unique_code}")
    else:
        logger.info(f"Using existing link for chat {chat_id}: {unique_code}")
    link = f"https://t.me/{BOT_USERNAME}?start={unique_code}"
    await message.answer(f"🔗 <b>Ваша уникальная ссылка:</b>\n\n{link}", parse_mode="HTML")