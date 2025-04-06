import asyncio
from aiogram import Dispatcher
from config import bot, REDIS_HOST, REDIS_PORT
from handlers import router
from aiogram.fsm.storage.redis import RedisStorage
import redis.asyncio as redis

# Use RedisStorage for persistent state management
storage = RedisStorage(redis=redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True))
dp = Dispatcher(bot=bot, storage=storage)

async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())