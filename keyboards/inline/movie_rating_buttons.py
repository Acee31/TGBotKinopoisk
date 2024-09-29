from typing import List, Dict
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_movie_rating_buttons(movie_data: List[Dict], limit: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()

    for index, movie in enumerate(movie_data[:limit]):
        title = movie.get('name', 'Неизвестно')
        raiting = movie.get('rating', {}).get('kp', 'Неизвестно')

        button_text = f'Название: {title}, рейтинг кинопоиска: {raiting}'

        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=f'movie_{index}'))

    return keyboard