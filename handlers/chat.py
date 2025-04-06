from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from states.anon_message import AnonMessage
from db.redis_db import save_chat_link, remove_chat_link, unlock_chat, get_chat_lock, redis_client
from utils.helpers import generate_unique_code
from config import BOT_USERNAME, logger, bot  # Added bot import

router = Router()

@router.message(Command("chat"))
async def start_chat(message: Message, state: FSMContext) -> None:
    owner_chat_id = message.chat.id
    chat_code = generate_unique_code()
    await save_chat_link(chat_code, owner_chat_id)
    await state.set_state(AnonMessage.chatting)
    current_state = await state.get_state()
    logger.info(f"Установлено состояние для {owner_chat_id}: {current_state}")
    link = f"https://t.me/{BOT_USERNAME}?start={chat_code}"
    await message.answer(
        f"💬 <b>Режим анонимного чата включён!</b>\n\n"
        f"Вот ваша ссылка для чата:\n{link}\n"
        "Первый, кто напишет, заблокирует чат для других. Для завершения используйте /stop_chat.",
        parse_mode="HTML"
    )
    logger.info(f"Chat mode enabled for {owner_chat_id} with link: {link}")

@router.message(Command("stop_chat"), AnonMessage.chatting)
async def stop_chat_in_chat(message: Message, state: FSMContext) -> None:
    chat_id = message.chat.id
    current_state = await state.get_state()
    if current_state != AnonMessage.chatting.state:
        await message.answer("❌ Вы не в режиме чата.")
        return

    # Проверяем, кто завершает чат: владелец или участник
    owner_chat_id = chat_id
    chat_code = await redis_client.get(f"chat_owner:{chat_id}")
    if chat_code:  # Это владелец чата
        sender_chat_id = await get_chat_lock(chat_id)
        if sender_chat_id:
            await bot.send_message(sender_chat_id, "🛑 Чат больше не существует. Владелец завершил сессию.", parse_mode="HTML")
        await remove_chat_link(chat_id)
        await unlock_chat(chat_id)
        await state.clear()
        await message.answer("🛑 <b>Чат завершён.</b> Ссылка удалена.", parse_mode="HTML")
        logger.info(f"Chat stopped by owner {chat_id}")
    else:  # Это участник чата
        for key in await redis_client.keys("chat_owner:*"):
            if await redis_client.get(key) == await redis_client.get(f"chat_link:{chat_id}"):
                owner_chat_id = int(key.split(":")[1])
                break
        await unlock_chat(owner_chat_id)
        await state.clear()
        await bot.send_message(owner_chat_id, "🛑 Участник завершил чат.", parse_mode="HTML")
        await message.answer("🛑 Вы вышли из чата.", parse_mode="HTML")
        logger.info(f"Chat stopped by participant {chat_id}")