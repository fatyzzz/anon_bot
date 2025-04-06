from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db.redis_db import redis_client
from config import BOT_USERNAME, logger

router = Router()

@router.message(Command("mylink"))
async def my_link(message: Message) -> None:
    unique_code = await redis_client.get(f"chat:{message.chat.id}")
    if unique_code:
        link = f"https://t.me/{BOT_USERNAME}?start={unique_code}"
        logger.info(f"Showing link: {link}")
        await message.answer(f"🔗 <b>Ваша текущая ссылка:</b>\n\n{link}", parse_mode="HTML")
    else:
        await message.answer("❌ У вас нет активной ссылки.")