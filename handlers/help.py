from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "<b>📚 Справка по боту:</b>\n\n"
        "- /getlink — получить уникальную ссылку\n"
        "- /revoke — отменить текущую ссылку\n"
        "- /mylink — показать текущую ссылку\n"
        "- /stats — показать статистику сообщений\n"
        "- /chat — включить режим анонимного чата\n"
        "- /stop_chat — выключить режим чата\n\n"
        "Поделитесь своей ссылкой, чтобы получать анонимные сообщения!",
        parse_mode="HTML"
    )