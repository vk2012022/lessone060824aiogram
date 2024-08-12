import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InputFile, FSInputFile, CallbackQuery
from aiogram import F
from gtts import gTTS
import os
from config import API_TOKEN
import random
# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
import keyboardsd1 as kb

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.callback_query(F.data == 'news')
async def news(callback: CallbackQuery):
    await callback.answer("Новости подгружаются", show_alert=True)
    await callback.message.edit_text('Вот свежие новости!', reply_markup=await kb.test_keyboard())


@dp.message(F.text == "Тестовая кнопка 1")
async def test_button(message: Message):
   await message.answer("Обработка нажатия на reply кнопку")


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Мои команды:\n /start \n /help")


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}', reply_markup=kb.inline_keyboard_test)



@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
