import telebot

bot = telebot.TeleBot('7401925570:AAG5cx2OQaqqb93gVLeB2Jq_KR46F553RqM')

@bot.message_handler(commands=['helloworld', 'start'])
def hello_word(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, 'Введи команду helloword')
        bot.register_next_step_handler(message, hello_word)
    elif message.text == '/helloword':
        bot.send_message(message.chat.id, 'Hello World!')

@bot.message_handler()
def hello(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}.')
    else:
        bot.send_message(message.chat.id, 'Я пока распознаю только сообщение - "Привет"')

bot.polling(none_stop=True)