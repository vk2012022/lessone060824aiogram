import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F

import random
# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = '7355440394:AAGqcHreAmY-DDmdHQrBNvz0ay0F_rJMQbU'

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()



@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("ИИ стал универсальным термином для приложений, которые выполняют сложные задачи, которые когда-то требовали участия человека, например, общение с клиентами в Интернете или игра в шахматы.")


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Мои команды:\n /start \n /help")


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer("ПРИВЕТИК")

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
