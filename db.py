import redis.asyncio as redis
from config import REDIS_HOST, REDIS_PORT

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

async def save_link(unique_code: str, chat_id: int) -> None:
    await redis_client.set(unique_code, chat_id)
    await redis_client.set(f"chat:{chat_id}", unique_code)

async def get_chat_id(unique_code: str) -> int | None:
    chat_id = await redis_client.get(unique_code)
    return int(chat_id) if chat_id else None

async def revoke_link(chat_id: int) -> None:
    unique_code = await redis_client.get(f"chat:{chat_id}")
    if unique_code:
        await redis_client.delete(unique_code)
        await redis_client.delete(f"chat:{chat_id}")

async def increment_stats(chat_id: int) -> None:
    await redis_client.incr(f"stats:{chat_id}")

async def get_stats(chat_id: int) -> int:
    stats = await redis_client.get(f"stats:{chat_id}")
    return int(stats) if stats else 0

async def set_message_sender(message_id: int, chat_id: int, sender_chat_id: int) -> None:
    key = f"message:{message_id}:{chat_id}"
    await redis_client.set(key, sender_chat_id)

async def get_message_sender(message_id: int, chat_id: int) -> int | None:
    key = f"message:{message_id}:{chat_id}"
    sender_chat_id = await redis_client.get(key)
    return int(sender_chat_id) if sender_chat_id else None