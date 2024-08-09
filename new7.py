import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3
import logging
from config import API_TOKEN  # Замените на ваш реальный API ключ

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)

class Form(StatesGroup):
    name = State()
    age = State()
    grade = State()
    confirmation = State()

def init_db():
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL)
    ''')
    conn.commit()
    conn.close()

# Инициализация базы данных
init_db()

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
    await message.answer("В каком ты классе?")
    await state.set_state(Form.grade)

@dp.message(Form.grade)
async def grade(message: Message, state: FSMContext):
    await state.update_data(grade=message.text)
    user_data = await state.get_data()

    # Сохранение данных пользователя в базу данных
    conn = sqlite3.connect('school_data.db')
    cur = conn.cursor()
    cur.execute('''
       INSERT INTO students (name, age, grade) VALUES (?, ?, ?)''',
                (user_data['name'], user_data['age'], user_data['grade']))
    conn.commit()
    conn.close()

    await message.answer("Данные сохранены. Хотите проверить правильность? (да/нет)")
    await state.set_state(Form.confirmation)

@dp.message(Form.confirmation)
async def confirm(message: Message, state: FSMContext):
    if message.text.lower() == 'да':
        user_data = await state.get_data()
        confirmation_message = (f"Сохраненные данные:\n"
                                f"Имя: {user_data['name']}\n"
                                f"Возраст: {user_data['age']}\n"
                                f"Класс: {user_data['grade']}\n\n"
                                f"Данные правильные? (да/нет)")
        await message.answer(confirmation_message)
        await state.set_state(Form.confirmation)
    elif message.text.lower() == 'нет':
        await message.answer("Пожалуйста, введите данные заново.")
        await state.set_state(Form.name)
    else:
        await message.answer("Ответ не распознан. Пожалуйста, ответьте 'да' или 'нет'.")
        await state.set_state(Form.confirmation)

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
