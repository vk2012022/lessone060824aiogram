import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message


from config import TOKEN

import random
from config import TOKEN

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command('photo'))
async def photo(message: Message):
    list1 = ['C:\Users\vk201\Documents\GitHub\lessone12html\img.png', 'C:\Users\vk201\Documents\GitHub\lessone12html\img_1.png', 'C:\Users\vk201\Documents\GitHub\lessone12html\img_2.png']
    rand_photo = random.choice(list1)
    await message.answer_photo(photo=rand_photo, caption='Это супер крутая картинка')

#Прописываем хендлер и варианты ответов:

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
    await message.answer("Мои команды: /start, /help")

@dp.message_handler(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())