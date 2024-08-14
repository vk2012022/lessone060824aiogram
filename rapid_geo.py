import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import requests

from config import API_TOKEN, RAPIDAPI_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функция для получения данных о городе с указанием страны
def get_city_data(city_name, country_code=None):
    url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
    querystring = {"namePrefix": city_name}

    if country_code:
        querystring["countryIds"] = country_code  # Добавляем код страны для более точного поиска

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        print(f"API response: {response.json()}")  # Отладка
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")  # Отладка
        return None


# Команда для получения данных о городе
@dp.message(Command("city"))
async def city_command(message: Message):
    print("Received city command")  # Отладка
    args = message.text.split(maxsplit=2)  # Разбиваем сообщение на части
    print(f"Args: {args}")  # Отладка

    if len(args) < 2:
        await message.answer("Пожалуйста, укажите название города после команды /city.\nПример: /city Paris")
        return

    city_name = args[1]  # Получаем название города
    country_code = args[2].upper() if len(args) > 2 else None  # Получаем код страны, если указан

    print(f"City name: {city_name}, Country code: {country_code}")  # Отладка

    city_data = get_city_data(city_name, country_code)
    print(f"City data: {city_data}")  # Отладка

    if city_data and 'data' in city_data and city_data['data']:
        city_info = city_data['data'][0]
        city_name = city_info['name']
        country = city_info['country']
        population = city_info.get('population', 'Информация о населении недоступна')
        latitude = city_info['latitude']
        longitude = city_info['longitude']
        await message.answer(
            f"Город: {city_name}\nСтрана: {country}\nНаселение: {population}\nКоординаты: {latitude}, {longitude}")
    else:
        await message.answer("Город не найден. Пожалуйста, проверьте название и попробуйте снова.")


# Команда /start
@dp.message(CommandStart())
async def start_command(message: Message):
    print("Received start command")  # Отладка
    await message.answer(
        "Привет! Используй команду /city <название города> <код страны (опционально)>, чтобы получить информацию о городе.")


# Обработка всех сообщений, которые не соответствуют зарегистрированным командам
@dp.message()
async def handle_invalid_command(message: Message):
    # Это будет обработчик сообщений, которые не подходят под команды
    await message.answer(
        "Команда введена неправильно или не поддерживается. Используйте /city <название города> <код страны (опционально)> для получения информации о городе.\nПример: /city Paris")


# Основной цикл бота
async def main():
    print("Bot is starting...")  # Отладка
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
