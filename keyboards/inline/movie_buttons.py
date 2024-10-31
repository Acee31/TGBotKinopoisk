from typing import List, Dict
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_movie_buttons(movie_data: List[Dict], limit: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for index, movie in enumerate(movie_data[:limit]):
        title = movie.get('name', 'Неизвестно')
        year = movie.get("year", "Неизвестно")

        button_text = f'Название: {title}, год выпуска: {year}'

        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=f'movie_{index}'))

    return keyboard