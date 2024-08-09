import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import aiohttp
import logging
import sqlite3
from config import API_TOKEN, WEATHER_API_KEY

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    city = State()

def init_db():
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    city TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

init_db()

async def get_weather(city):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json(), None
            else:
                return None, "Ошибка получения данных о погоде. Пожалуйста, проверьте название города и попробуйте снова."

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Привет! Как тебя зовут?")
    await state.set_state(Form.name)

@dp.message(Form.name)
async def name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Сколько тебе лет?")
    await state.set_state(Form.age)

@dp.message(Form.age)
async def age(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("Из какого ты города?")
    await state.set_state(Form.city)

@dp.message(Form.city)
async def city(message: Message, state: FSMContext):
    await state.update_data(city=message.text)
    user_data = await state.get_data()

    # Сохраняем данные пользователя в БД
    conn = sqlite3.connect('user_data.db')
    cur = conn.cursor()
    cur.execute('''
       INSERT INTO users (name, age, city) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['city']))
    conn.commit()
    conn.close()

    # Получаем данные о погоде
    weather_data, error = await get_weather(user_data['city'])
    if error:
        await message.answer(error)
    else:
        main = weather_data['main']
        weather = weather_data['weather'][0]

        temperature = main['temp']
        humidity = main['humidity']
        description = weather['description']

        weather_report = (f"Город - {user_data['city']}\n"
                          f"Температура - {temperature}°C\n"
                          f"Влажность воздуха - {humidity}%\n"
                          f"Описание погоды - {description}")

        await message.answer(weather_report)

    await state.clear()

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
