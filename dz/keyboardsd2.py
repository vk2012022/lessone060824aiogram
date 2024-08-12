from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Создаем меню с кнопками "Привет" и "Пока"
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ],
    resize_keyboard=True
)

# Создаем инлайн-кнопки с ссылками
links_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Новости", url="https://news.ycombinator.com/")],
    [InlineKeyboardButton(text="Музыка", url="https://www.spotify.com/")],
    [InlineKeyboardButton(text="Видео", url="https://www.youtube.com/")]
])

# Инлайн-кнопка "Показать больше"
show_more_button = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
])

# Функция для создания кнопок "Опция 1" и "Опция 2"
def create_options_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])
