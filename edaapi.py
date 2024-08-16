import asyncio
import json  # Для работы с сохранением и загрузкой переводов
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import requests
from config5 import API_TOKEN, EDAMAM_APP_ID, EDAMAM_APP_KEY
from googletrans import Translator  # Импортируем Google Translate API

# Конфигурация токена бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Инициализация переводчика
translator = Translator()

# Путь к файлу с пользовательскими переводами
TRANSLATIONS_FILE = "translations.json"

# Базовый словарь для часто используемых слов
manual_translation = {
    "рис": "rice",
    "курица": "chicken"
}


# Функция для загрузки пользовательских переводов из файла
def load_translations():
    try:
        with open(TRANSLATIONS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Функция для сохранения пользовательских переводов в файл
def save_translations(translations):
    with open(TRANSLATIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(translations, file, ensure_ascii=False, indent=4)


# Загружаем пользовательские переводы
user_translations = load_translations()


# Объединяем базовый и пользовательский словари
def get_combined_translations():
    combined = manual_translation.copy()
    combined.update(user_translations)
    return combined


# Функция для исправления известных переводов
def correct_translation(word):
    combined_translations = get_combined_translations()
    # Если слово в словаре, возвращаем правильный перевод
    return combined_translations.get(word.lower(), word)


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
        ingredients = query[1].split(", ")  # Разделяем ингредиенты
        translated_ingredients = []

        for ingredient in ingredients:
            # Проверяем каждый ингредиент в словаре и переводим при необходимости
            corrected_ingredient = correct_translation(ingredient)
            if corrected_ingredient == ingredient:  # Если ингредиент не в словаре, переводим
                corrected_ingredient = translator.translate(ingredient, src='ru',
                                                            dest='en').text.lower()  # Принудительно в нижний регистр
            translated_ingredients.append(corrected_ingredient)

        query_translated = ", ".join(translated_ingredients)  # Объединяем переведенные ингредиенты
        print(f"Переведенный запрос: {query_translated}")  # Выводим переведенный запрос для диагностики
        recipes = search_recipes(query_translated)
        if recipes and recipes['hits']:
            for hit in recipes['hits']:
                recipe = hit['recipe']
                title = recipe['label']
                url = recipe['url']

                # Переводим название рецепта на русский
                title_ru = translator.translate(title, src='en', dest='ru').text

                await message.answer(f"Рецепт: {title_ru}\nСсылка: {url}\n")
        else:
            await message.answer("Рецепты не найдены.")
            print(f"Ответ от API: {recipes}")  # Выводим ответ от API для отладки
    else:
        await message.answer("Пожалуйста, укажите ингредиенты для поиска. Пример: /recipe курица, рис")


# Команда для добавления нового перевода
@dp.message(Command("add_translation"))
async def add_translation_command(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        try:
            # Ожидаем формат: /add_translation <русское слово>:<английский перевод>
            new_translation = args[1].split(":")
            if len(new_translation) == 2:
                russian_word = new_translation[0].strip().lower()
                english_word = new_translation[1].strip().lower()

                # Добавляем перевод в пользовательский словарь
                user_translations[russian_word] = english_word
                save_translations(user_translations)  # Сохраняем в файл

                await message.answer(f"Перевод добавлен: {russian_word} -> {english_word}")
            else:
                await message.answer(
                    "Формат команды неправильный. Используйте: /add_translation <русское слово>:<английский перевод>")
        except Exception as e:
            await message.answer(f"Ошибка при добавлении перевода: {e}")
    else:
        await message.answer(
            "Пожалуйста, укажите перевод в формате: /add_translation <русское слово>:<английский перевод>")


# Команда для просмотра всего словаря
@dp.message(Command("show_dictionary"))
async def show_dictionary_command(message: types.Message):
    combined_translations = get_combined_translations()
    base_translations = manual_translation
    user_translations_str = '\n'.join([f"{k}: {v}" for k, v in user_translations.items()])

    await message.answer(f"Базовый словарь:\n{base_translations}\n\n"
                         f"Пользовательский словарь:\n{user_translations_str}")


# Команда для редактирования перевода
@dp.message(Command("edit_translation"))
async def edit_translation_command(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        try:
            # Ожидаем формат: /edit_translation <русское слово>:<новый английский перевод>
            edit_translation = args[1].split(":")
            if len(edit_translation) == 2:
                russian_word = edit_translation[0].strip().lower()
                new_english_word = edit_translation[1].strip().lower()

                if russian_word in user_translations:
                    # Обновляем перевод
                    user_translations[russian_word] = new_english_word
                    save_translations(user_translations)  # Сохраняем в файл
                    await message.answer(f"Перевод обновлен: {russian_word} -> {new_english_word}")
                else:
                    await message.answer(f"Слово '{russian_word}' не найдено в пользовательском словаре.")
            else:
                await message.answer(
                    "Формат команды неправильный. Используйте: /edit_translation <русское слово>:<новый английский перевод>")
        except Exception as e:
            await message.answer(f"Ошибка при изменении перевода: {e}")
    else:
        await message.answer(
            "Пожалуйста, укажите перевод в формате: /edit_translation <русское слово>:<новый английский перевод>")


# Команда для удаления перевода
@dp.message(Command("remove_translation"))
async def remove_translation_command(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) == 2:
        russian_word = args[1].strip().lower()
        if russian_word in user_translations:
            del user_translations[russian_word]
            save_translations(user_translations)  # Сохраняем изменения в файл
            await message.answer(f"Перевод удален: {russian_word}")
        else:
            await message.answer(f"Слово '{russian_word}' не найдено в пользовательском словаре.")
    else:
        await message.answer("Пожалуйста, укажите слово для удаления. Пример: /remove_translation <русское слово>")


# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Я могу помочь найти рецепты на основе ингредиентов.\n"
                         "Используйте команду /recipe <ингредиенты>, чтобы найти рецепт.\n"
                         "Пример: /recipe курица, рис\n"
                         "Для добавления нового перевода ингредиента используйте: /add_translation <русское слово>:<английский перевод>\n"
                         "Для просмотра словаря используйте: /show_dictionary\n"
                         "Для изменения перевода: /edit_translation <русское слово>:<новый английский перевод>\n"
                         "Для удаления перевода: /remove_translation <русское слово>\n"
                         "Для справки: /help")


# Команда /help для вывода справочной информации
@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Список доступных команд:\n"
                         "/recipe <ингредиенты> - поиск рецептов по ингредиентам\n"
                         "/add_translation <русское слово>:<английский перевод> - добавление нового перевода\n"
                         "/edit_translation <русское слово>:<новый английский перевод> - редактирование перевода\n"
                         "/remove_translation <русское слово> - удаление перевода\n"
                         "/show_dictionary - просмотр словаря\n"
                         "/start - запуск бота\n"
                         "/help - справка")


# Обработка неизвестных команд
@dp.message()
async def unknown_command(message: types.Message):
    await message.answer("Неизвестная команда. Пожалуйста, используйте /help для просмотра списка команд.")


# Основной цикл бота
async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
