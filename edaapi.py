import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests

# Ваши ключи от Edamam API (полученные при регистрации)
EDAMAM_APP_ID = 'c3ee9338'
EDAMAM_APP_KEY = '209070d5e5b592d0c6e38ed9e901e0d7'

# Конфигурация токена бота
API_TOKEN = '7355440394:AAGqcHreAmY-DDmdHQrBNvz0ay0F_rJMQbU'

# Создаем экземпляр бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функция для поиска рецептов через Edamam API
def search_recipes(query):
    url = "https://api.edamam.com/search"
    params = {
        "q": query,
        "app_id": EDAMAM_APP_ID,
        "app_key": EDAMAM_APP_KEY,
        "to": 5  # Ограничение количества результатов (до 5 рецептов)
    }
    response = requests.get(url, params=params)

    # Проверка статуса ответа
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка API: {response.status_code}")
        return None


# Команда для поиска рецептов по ингредиентам
@dp.message(Command("recipe"))
async def recipe_command(message: types.Message):
    query = message.text.split(maxsplit=1)  # Извлекаем запрос после команды /recipe
    if len(query) == 2:
        recipes = search_recipes(query[1])
        if recipes and recipes['hits']:
            for hit in recipes['hits']:
                recipe = hit['recipe']
                title = recipe['label']
                url = recipe['url']
                await message.answer(f"Рецепт: {title}\nСсылка: {url}\n")
        else:
            await message.answer("Рецепты не найдены.")
    else:
        await message.answer("Пожалуйста, укажите ингредиенты для поиска. Пример: /recipe chicken, rice")


# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я могу помочь найти рецепты на основе ингредиентов.\n"
                         "Используйте команду /recipe <ингредиенты>, чтобы найти рецепт.\n"
                         "Пример: /recipe chicken, rice")


# Основной цикл бота
async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
