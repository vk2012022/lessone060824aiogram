import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from googletrans import Translator
from config import API_TOKEN


bot = Bot(token=API_TOKEN)
dp = Dispatcher()
translator = Translator()

# Функция для перевода текста на русский
def translate_to_russian(text):
    try:
        translation = translator.translate(text, dest='ru')
        return translation.text
    except Exception as e:
        print(f"Ошибка при переводе: {e}")
        return text

# Функция для получения данных о нескольких постах
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Функция для получения данных о пользователях
def get_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Команда для получения нескольких постов с переводом
@dp.message(Command("posts"))
async def posts_command(message: types.Message):
    posts = get_posts()
    if posts:
        for post in posts[:5]:  # Ограничиваем вывод до 5 постов
            title_ru = translate_to_russian(post['title'])
            body_ru = translate_to_russian(post['body'])
            await message.answer(f"Заголовок: {title_ru}\nТекст: {body_ru}\n")
    else:
        await message.answer("Ошибка при получении постов. Попробуйте позже.")

# Команда для получения списка пользователей с переводом на русский
@dp.message(Command("users"))
async def users_command(message: types.Message):
    users = get_users()
    if users:
        for user in users[:5]:  # Ограничиваем вывод до 5 пользователей
            name_ru = translate_to_russian(user['name'])
            email = user['email']
            website = user['website']
            await message.answer(f"Пользователь: {name_ru}\nEmail: {email}\nСайт: {website}\n")
    else:
        await message.answer("Ошибка при получении пользователей. Попробуйте позже.")

# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я могу получить данные из JSONPlaceholder и перевести их на русский.\n"
                         "Доступные команды:\n"
                         "/posts - получить и перевести список постов\n"
                         "/users - получить и перевести список пользователей.")

# Основной цикл бота
async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
