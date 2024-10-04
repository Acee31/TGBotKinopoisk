from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}! Я бот по поиску информации о фильмах и сериалах.\n"
                          f"Выбери команду из списка ниже.")
