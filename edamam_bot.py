import asyncio
import requests
from googletrans import Translator  # Импортируем переводчик
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config3 import API_TOKEN, EDAMAM_APP_ID, EDAMAM_APP_KEY

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()


# Функция для анализа питания
def get_nutrition_data(query):
    # Переводим запрос с русского на английский
    translated_query = translator.translate(query, src='ru', dest='en').text

    url = f'https://api.edamam.com/api/nutrition-data'
    params = {
        'app_id': EDAMAM_APP_ID,
        'app_key': EDAMAM_APP_KEY,
        'ingr': translated_query
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Ошибка при запросе к API Edamam"}


# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Введи ингредиенты или блюдо, чтобы узнать его пищевую ценность.")


# Обработка сообщений с запросом к Edamam API
@dp.message()
async def handle_message(message: Message):
    query = message.text
    data = get_nutrition_data(query)

    if "error" in data:
        await message.answer(data["error"])
    else:
        # Извлекаем информацию о калориях и других питательных веществах
        calories = data.get('calories', 'Нет данных')
        total_weight = data.get('totalWeight', 'Нет данных')
        nutrients = data.get('totalNutrients', {})

        response_text = f"Пищевая ценность для '{query}':\n"
        response_text += f"Калории: {calories} ккал\n"
        response_text += f"Вес: {total_weight} г\n"

        # Добавляем информацию о ключевых питательных веществах
        if 'FAT' in nutrients:
            response_text += f"Жиры: {nutrients['FAT']['quantity']:.2f} г\n"
        if 'CHOCDF' in nutrients:
            response_text += f"Углеводы: {nutrients['CHOCDF']['quantity']:.2f} г\n"
        if 'PROCNT' in nutrients:
            response_text += f"Белки: {nutrients['PROCNT']['quantity']:.2f} г\n"

        await message.answer(response_text)


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
