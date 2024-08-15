import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests

from config import API_TOKEN, RAPIDAPI_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функция для получения информации о фильме
def get_movie_data(movie_title):
    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {"s": movie_title, "r": "json", "type": "movie"}
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        movie_data = response.json()
        print(f"API response: {movie_data}")  # Отладка - вывод полного ответа от API
        return movie_data
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")  # Вывод ошибки при неудачном запросе
        return None


# Команда для получения информации о фильме
@dp.message(Command("movie"))
async def movie_command(message: Message):
    args = message.text.split(maxsplit=1)  # Получаем аргументы команды
    if len(args) < 2:
        await message.answer("Пожалуйста, укажите название фильма после команды /movie.")
        return

    movie_title = args[1]  # Название фильма
    movie_data = get_movie_data(movie_title)

    # Проверяем, есть ли данные о фильме
    if movie_data and movie_data.get('Response') == 'True':
        movie_info = movie_data['Search'][0]  # Берем первый найденный фильм
        title = movie_info['Title']
        year = movie_info['Year']
        type = movie_info['Type']
        await message.answer(f"Название: {title}\nГод: {year}\nТип: {type}")
    else:
        await message.answer("Фильм не найден. Пожалуйста, проверьте название и попробуйте снова.")


# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Привет! Используй команду /movie <название фильма>, чтобы получить информацию о фильме.")


# Основной цикл бота
async def main():
    print("Bot is starting...")  # Отладка
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
