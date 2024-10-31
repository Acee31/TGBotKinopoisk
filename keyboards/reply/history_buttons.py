from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def create_history_buttons():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    button_all_time = KeyboardButton("За весь период")
    button_specific_date = KeyboardButton("Уточнить дату")

    markup.add(button_all_time, button_specific_date)
    return markup