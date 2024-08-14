import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests
from googletrans import Translator

from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# Функция для получения случайного совета с Advice Slip API
def get_random_advice():
    url = "https://api.adviceslip.com/advice"
    response = requests.get(url)
    advice_data = response.json()
    return advice_data['slip']['advice']

# Команда для получения случайного совета и его перевода на русский язык
@dp.message(Command("advice"))
async def random_advice(message: Message):
    advice = get_random_advice()
    translated_advice = translator.translate(advice, dest='ru').text
    await message.answer(f"💡 Совет: {translated_advice}")

# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Напиши команду /advice, чтобы получить случайный совет по здоровью.")

# Основной цикл бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
