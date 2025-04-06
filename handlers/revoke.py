from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from db import revoke_link

router = Router()

@router.message(Command("revoke"))
async def revoke_link_command(message: Message) -> None:
    await revoke_link(message.chat.id)
    await message.answer("🗑️ Ваша ссылка отменена.")