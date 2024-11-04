from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_types_button() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("Фильм", callback_data="movie"),
        InlineKeyboardButton("Сериал", callback_data="series"),
        InlineKeyboardButton("Мультфильм", callback_data="cartoon"),
        InlineKeyboardButton("Анимационный сериал", callback_data="animated_series"),
        InlineKeyboardButton("Аниме", callback_data="anime")
    ]
    markup.add(*buttons)
    return markup
