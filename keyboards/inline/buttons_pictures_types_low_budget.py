from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_types_button_for_budget() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("Фильм", callback_data="budget_movie"),
        InlineKeyboardButton("Сериал", callback_data="budget_series"),
        InlineKeyboardButton("Мультфильм", callback_data="budget_cartoon"),
        InlineKeyboardButton("Анимационный сериал", callback_data="budget_animated_series"),
        InlineKeyboardButton("Аниме", callback_data="budget_anime")
    ]
    markup.add(*buttons)
    return markup
