import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from config1 import API_TOKEN
import keyboardsd2 as kb

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    print("Команда /start получена")  # Отладочное сообщение
    await message.answer("Добро пожаловать! Выберите команду:", reply_markup=kb.main_menu)

# Обработчик команды /help
@dp.message(Command("help"))
async def send_help(message: Message):
    print("Команда /help получена")  # Отладочное сообщение
    help_text = (
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать справку по доступным командам\n"
        "/links - Показать инлайн-кнопки с ссылками\n"
        "/dynamic - Показать динамическую кнопку 'Показать больше'\n"
    )
    await message.answer(help_text)

# Обработчик нажатия кнопки "Привет"
@dp.message(lambda message: message.text == "Привет")
async def greet_user(message: Message):
    print("Нажата кнопка 'Привет'")  # Отладочное сообщение
    await message.answer(f"Привет, {message.from_user.full_name}!")

# Обработчик нажатия кнопки "Пока"
@dp.message(lambda message: message.text == "Пока")
async def say_goodbye(message: Message):
    print("Нажата кнопка 'Пока'")  # Отладочное сообщение
    await message.answer(f"До свидания, {message.from_user.full_name}!")

# Обработчик команды /links
@dp.message(Command("links"))
async def send_links(message: Message):
    print("Команда /links получена")  # Отладочное сообщение
    await message.answer("Выберите ссылку:", reply_markup=kb.links_menu)

# Обработчик команды /dynamic
@dp.message(Command("dynamic"))
async def send_dynamic(message: Message):
    print("Команда /dynamic получена")  # Отладочное сообщение
    await message.answer("Нажмите на кнопку ниже:", reply_markup=kb.show_more_button)

# Обработчик нажатия на кнопку "Показать больше"
@dp.callback_query(lambda c: c.data == "show_more")
async def show_more_options(callback_query: CallbackQuery):
    print("Нажата кнопка 'Показать больше'")  # Отладочное сообщение
    await callback_query.message.edit_reply_markup(reply_markup=kb.create_options_menu())

# Обработчик нажатия на кнопку "Опция 1"
@dp.callback_query(lambda c: c.data == "option_1")
async def option_1_selected(callback_query: CallbackQuery):
    print("Нажата кнопка 'Опция 1'")  # Отладочное сообщение
    await callback_query.answer("Вы выбрали Опция 1", show_alert=True)

# Обработчик нажатия на кнопку "Опция 2"
@dp.callback_query(lambda c: c.data == "option_2")
async def option_2_selected(callback_query: CallbackQuery):
    print("Нажата кнопка 'Опция 2'")  # Отладочное сообщение
    await callback_query.answer("Вы выбрали Опция 2", show_alert=True)

async def main():
    print("Бот запущен")  # Отладочное сообщение
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
