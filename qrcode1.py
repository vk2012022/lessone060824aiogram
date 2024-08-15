import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import requests
import base64
import os

from config import API_TOKEN, RAPIDAPI_KEY

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


# Функция для генерации QR-кода через API QRCode Monkey с отладочным выводом
def generate_qr_code(encoded_string):
    url = "https://qrcode-monkey.p.rapidapi.com/qr/uploadImage"

    payload = {
        "image": encoded_string,
        "quality": "high"
    }

    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": "qrcode-monkey.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    # Отладка: выводим статус и полный ответ от API
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Content: {response.text}")

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


# Обработка изображения от пользователя
@dp.message(F.content_type == "photo")
async def handle_image(message: types.Message):
    photo = message.photo[-1]  # Получаем изображение наивысшего качества
    file_info = await bot.get_file(photo.file_id)
    downloaded_file = await bot.download_file(file_info.file_path)

    # Сохраняем изображение во временный файл
    with open("temp_image.png", "wb") as new_file:
        new_file.write(downloaded_file.getvalue())

    # Открываем файл и кодируем его в base64
    with open("temp_image.png", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")

    # Генерируем QR-код через API
    qr_result = generate_qr_code(encoded_string)

    # Удаляем временное изображение после использования
    os.remove("temp_image.png")

    if qr_result:
        await message.answer("QR-код успешно сгенерирован! Вот результат:")
        await message.answer(qr_result)  # Вывод результата
    else:
        await message.answer("Ошибка при генерации QR-кода. Попробуйте снова.")


# Команда /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Отправь мне изображение, чтобы я сгенерировал QR-код.")


# Основной цикл бота
async def main():
    print("Bot is starting...")  # Отладка
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
