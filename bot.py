import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

#logging.basicConfig(level=logging.INFO)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
