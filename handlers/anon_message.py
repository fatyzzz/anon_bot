from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey  # Added for proper FSM key creation
from states.anon_message import AnonMessage
from db.redis_db import get_chat_id, increment_stats, set_message_sender, lock_chat, is_chat_locked, get_chat_lock
from utils.helpers import format_message
from keyboards.reply import get_reply_keyboard
from config import logger, bot  # Added bot import

router = Router()

@router.message(AnonMessage.sending_message)
async def send_anon_message(message: Message, state: FSMContext) -> None:
    """Handle sending an anonymous message or chat message to a target user."""
    data = await state.get_data()
    unique_code = data.get("unique_code")
    target_chat_id = data.get("target_chat_id")

    if not target_chat_id:
        await message.answer("❌ Ошибка: цель не определена.")
        await state.clear()
        return

    sender_chat_id = message.chat.id

    # Create a proper StorageKey for the recipient's FSM context
    recipient_key = StorageKey(bot_id=bot.id, chat_id=target_chat_id, user_id=target_chat_id)
    recipient_fsm = FSMContext(storage=state.storage, key=recipient_key)
    recipient_state = await recipient_fsm.get_state()
    logger.info(f"Recipient {target_chat_id} state: {recipient_state}")

    if await is_chat_locked(target_chat_id):
        locked_sender = await get_chat_lock(target_chat_id)
        if sender_chat_id != locked_sender:
            await message.answer("🚫 Чат занят другим пользователем. Попробуйте позже.")
            await state.clear()
            return

    if recipient_state == AnonMessage.chatting.state:
        # Chat mode
        if not await is_chat_locked(target_chat_id):
            await lock_chat(target_chat_id, sender_chat_id)
            await bot.send_message(target_chat_id, "💬 Новый участник подключился к чату!", parse_mode="HTML")
            logger.info(f"Chat locked for {target_chat_id} with sender {sender_chat_id}")
            await state.set_state(AnonMessage.chatting)  # Set state for sender (B)
            await state.update_data(chatting_with=target_chat_id)
            await recipient_fsm.update_data(chatting_with=sender_chat_id)

        if message.text:
            formatted_text = format_message(message.text)
            await bot.send_message(target_chat_id, formatted_text, parse_mode="HTML")
        elif message.photo:
            caption = format_message("📷 Фото")
            await bot.send_photo(target_chat_id, message.photo[-1].file_id, caption=caption, parse_mode="HTML")
        elif message.video:
            caption = format_message("🎥 Видео")
            await bot.send_video(target_chat_id, message.video.file_id, caption=caption, parse_mode="HTML")
        elif message.audio:
            caption = format_message("🎵 Аудио")
            await bot.send_audio(target_chat_id, message.audio.file_id, caption=caption, parse_mode="HTML")
        elif message.document:
            caption = format_message("📄 Документ")
            await bot.send_document(target_chat_id, message.document.file_id, caption=caption, parse_mode="HTML")
        else:
            await message.answer("❌ Неподдерживаемый тип сообщения.")
            await state.clear()
            return
        await message.answer("💬 Сообщение отправлено в чат.")
        await state.update_data(chat_id=target_chat_id)
    else:
        # Normal anonymous mode
        if message.text:
            formatted_text = format_message(message.text)
            sent_message = await bot.send_message(
                target_chat_id, formatted_text, parse_mode="HTML", reply_markup=get_reply_keyboard()
            )
        elif message.photo:
            caption = format_message("📷 Фото")
            sent_message = await bot.send_photo(
                target_chat_id, message.photo[-1].file_id, caption=caption, parse_mode="HTML",
                reply_markup=get_reply_keyboard()
            )
        elif message.video:
            caption = format_message("🎥 Видео")
            sent_message = await bot.send_video(
                target_chat_id, message.video.file_id, caption=caption, parse_mode="HTML",
                reply_markup=get_reply_keyboard()
            )
        elif message.audio:
            caption = format_message("🎵 Аудио")
            sent_message = await bot.send_audio(
                target_chat_id, message.audio.file_id, caption=caption, parse_mode="HTML",
                reply_markup=get_reply_keyboard()
            )
        elif message.document:
            caption = format_message("📄 Документ")
            sent_message = await bot.send_document(
                target_chat_id, message.document.file_id, caption=caption, parse_mode="HTML",
                reply_markup=get_reply_keyboard()
            )
        else:
            await message.answer("❌ Неподдерживаемый тип сообщения.")
            await state.clear()
            return
        await set_message_sender(sent_message.message_id, target_chat_id, sender_chat_id)
        await message.answer("✅ Сообщение отправлено анонимно.")

    await increment_stats(target_chat_id)
    logger.info(f"Message sent from {sender_chat_id} to {target_chat_id}")
    # Do not clear state to allow continued messaging in chat mode

@router.message(AnonMessage.chatting, ~F.text.startswith('/'))
async def handle_chat_message(message: Message, state: FSMContext) -> None:
    """Обрабатывает сообщения в чате, исключая команды."""
    data = await state.get_data()
    chatting_with = data.get("chatting_with")
    if not chatting_with:
        await message.answer("❌ Чат не активен.")
        return
    formatted_text = f"💬 <b>Сообщение в чате:</b>\n\n{message.text}"
    await bot.send_message(chatting_with, formatted_text, parse_mode="HTML")
    await message.answer("💬 Сообщение отправлено в чат.")