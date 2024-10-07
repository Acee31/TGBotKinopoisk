from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_types_button_for_h_budget() -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup()
    buttons = [
        InlineKeyboardButton("Фильм", callback_data="budget_h_movie"),
        InlineKeyboardButton("Сериал", callback_data="budget_h_series"),
        InlineKeyboardButton("Мультфильм", callback_data="budget_h_cartoon"),
        InlineKeyboardButton("Анимационный сериал", callback_data="budget_h_animated_series"),
        InlineKeyboardButton("Аниме", callback_data="budget_h_anime")
    ]
    markup.add(*buttons)
    return markup
