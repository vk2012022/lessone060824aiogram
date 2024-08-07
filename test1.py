import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InputFile, FSInputFile
from aiogram import F
from gtts import gTTS
import os

import random
# Замените 'YOUR_BOT_TOKEN' на токен вашего бота
API_TOKEN = '7355440394:AAGqcHreAmY-DDmdHQrBNvz0ay0F_rJMQbU'

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


@dp.message(Command('doc'))
async def doc(message: Message):
	doc = FSInputFile("Еще один важный файл (1).pdf")
	await bot.send_document(message.chat.id, doc)

@dp.message(Command("video"))
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')
    video = FSInputFile('Запись 2024-06-12 171731.mp4')
    await bot.send_video(message.chat.id, video)

@dp.message(Command("audio"))
async def audio(message: Message):
    audio = FSInputFile('antonio-vivaldi-concerto-no-2-in-g-minor-op-8-rv-315-lestate-iii-prest.mp3')
    await bot.send_audio(message.chat.id, audio)

@dp.message(Command('voice'))
async def voice(message: Message):
    voice = FSInputFile("uvedomlenie-o-poluchennoy-pochte.ogg")
    await message.answer_voice(voice)

@dp.message(Command('training'))
async def training(message: Message):
   training_list = [
       "Тренировка 1:\\n1. Скручивания: 3 подхода по 15 повторений\\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\\n1. Подъемы ног: 3 подхода по 15 повторений\\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)
   await message.answer(f"Это ваша мини-тренировка на сегодня {rand_tr}")

   tts = gTTS(text=rand_tr, lang='ru')
   tts.save('training.mp3')

   audio = FSInputFile('training.mp3')
   await bot.send_audio(message.chat.id, audio)
   os.remove("training.mp3")

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg')

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("ИИ стал универсальным термином для приложений, которые выполняют сложные задачи, которые когда-то требовали участия человека, например, общение с клиентами в Интернете или игра в шахматы.")


@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("Мои команды:\n /start \n /help")


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f'Приветики, {message.from_user.full_name}')



@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
