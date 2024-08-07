import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram import F
from gtts import gTTS
from googletrans import Translator
import os
import random
from config import API_TOKEN

# Создаем объект бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

translator = Translator()

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

@dp.message(Command('send_voice'))
async def send_voice(message: Message):
    text_to_convert = message.text[11:].strip()  # Получаем текст после команды /send_voice
    if text_to_convert:
        tts = gTTS(text=text_to_convert, lang='ru')
        tts.save('voice_message.ogg')

        voice = FSInputFile('voice_message.ogg')
        await bot.send_voice(message.chat.id, voice)
        os.remove('voice_message.ogg')
    else:
        await message.answer("Пожалуйста, предоставьте текст для голосового сообщения после команды /send_voice")

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
    if not os.path.exists('img'):
        os.makedirs('img')
    await bot.download(message.photo[-1], destination=f'img/{message.photo[-1].file_id}.jpg')
    await message.answer("Фото сохранено!")

@dp.message(F.text == "Что такое ИИ?")
async def aitext(message: Message):
    await message.answer("ИИ стал универсальным термином для приложений, которые выполняют сложные задачи, которые когда-то требовали участия человека, например, общение с клиентами в Интернете или игра в шахматы.")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer(
        "Мои команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать это сообщение\n"
        "/doc - Отправить документ\n"
        "/video - Отправить видео\n"
        "/audio - Отправить аудио\n"
        "/voice - Отправить голосовое сообщение\n"
        "/send_voice <текст> - Отправить голосовое сообщение с указанным текстом\n"
        "/training - Отправить тренировку на сегодня\n"
    )

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(f'Приветики, {message.from_user.full_name}')

@dp.message(F.text)
async def translate_text(message: Message):
    translated = translator.translate(message.text, dest='en')
    await message.answer(f'Translated text: {translated.text}')

@dp.message()
async def start(message: Message):
    await message.send_copy(chat_id=message.chat.id)

async def main():
    # Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
