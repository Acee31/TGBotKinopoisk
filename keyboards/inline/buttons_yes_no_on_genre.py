from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_yes_no_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("Да", callback_data='yes_genre'),
        InlineKeyboardButton("Нет", callback_data='no_genre')
    )

    return keyboard