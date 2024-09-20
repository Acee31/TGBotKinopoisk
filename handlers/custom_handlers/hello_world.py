from telebot.types import Message

from loader import bot

@bot.message_handler(commands=['hello_world'])
def hello_world(message: Message):
    bot.reply_to(message, 'Привет, мир!')

@bot.message_handler(func=lambda message: message.text.lower() == 'привет')
def hello(message: Message):
    bot.reply_to(message, 'Привет')