from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db import get_stats

router = Router()

@router.message(Command("stats"))
async def stats(message: Message) -> None:
    chat_id = message.chat.id
    stats = await get_stats(chat_id)
    await message.answer(f"📊 <b>Статистика:</b>\n\nВы получили {stats} анонимных сообщений.", parse_mode="HTML")