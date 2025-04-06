import os
import logging
from dotenv import load_dotenv
from aiogram import Bot

load_dotenv()

BOT_TOKEN: str = os.getenv("BOT_TOKEN")
REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
BOT_USERNAME: str = os.getenv("BOT_USERNAME")  # Берется из .env

# Проверки настроек
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN must be set in .env")
if not BOT_USERNAME:
    raise ValueError("BOT_USERNAME must be set in .env")
if BOT_USERNAME.startswith("@"):
    raise ValueError("BOT_USERNAME in .env should not start with '@'")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем объект bot
bot = Bot(token=BOT_TOKEN)