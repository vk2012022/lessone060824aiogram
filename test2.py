import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import requests

# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = '7355440394:AAGqcHreAmY-DDmdHQrBNvz0ay0F_rJMQbU'
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# API ключ для OpenWeatherMap
API_KEY = "3fef74ee2c56c7e1881a503252d7ceaf"


@dp.message(Command("weather"))
async def send_weather(message: Message):
    city = "Москва"  # Фиксируем город Москва
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        weather_info = (
            f"Погода в {data['name']}:\n"
            f"Температура: {data['main']['temp']}°C\n"
            f"Погода: {data['weather'][0]['description']}"
        )
        await message.answer(weather_info)
    else:
        await message.answer("Ошибка получения данных о погоде.")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Мои команды:\n /start \n /help \n /weather")
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("ПРИВЕТ! Используйте команду /weather, чтобы узнать погоду в Москве.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
