from datetime import datetime
from telebot.states.sync.context import StateContext
from peewee import fn
from database.models import History, User
from telebot.types import Message
from keyboards.reply.history_buttons import create_history_buttons
from states.user_data import UserInputInfo
from loader import bot
from telegram_bot_pagination import InlineKeyboardPaginator
from handlers.custom_handlers.callback.callback_history import format_history_record
from handlers.custom_handlers.movie_search import any_state


@bot.message_handler(commands=["history"])
def send_history(message: Message):
    user_id = message.from_user.id

    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Выполните команду /start")
        return

    markup = create_history_buttons()
    bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ["За весь период", "Уточнить дату"])
def handle_history_option(message: Message, state: StateContext):
    user_id = message.from_user.id

    if message.text == "За весь период":
        user = User.get(User.user_id == user_id)
        history_records = History.select().where(History.user == user).order_by(History.search_date.desc())

        page_count = history_records.count()

        if page_count == 0:
            bot.send_message(message.chat.id, "История запросов пуста. Введите новую команду.")
            return

        paginator = InlineKeyboardPaginator(
            page_count,
            current_page=1,
            data_pattern="history#{page}"
        )

        record = history_records[0]
        result = format_history_record(record)

        bot.send_message(message.chat.id, result, reply_markup=paginator.markup)

    elif message.text == "Уточнить дату":
        bot.send_message(message.chat.id, "Введите дату в формате \nГод-Месяц-День\nдля просмотра истории запросов.\n"
                                          "Или введите /cancel для сброса")
        state.set(UserInputInfo.waiting_for_date)


@bot.message_handler(state=UserInputInfo.waiting_for_date)
def get_history_for_date(message: Message, state):
    user_id = message.from_user.id
    input_date = message.text

    if input_date == "/cancel":
        any_state(message)

    try:
        specified_date = datetime.strptime(input_date, "%Y-%m-%d").date()
    except ValueError:
        bot.send_message(message.chat.id, "Неверный формат. Пожалуйста используйте формат даты \nГод-Месяц-День\n"
                                          "или выберите /cancel")
        return

    user = User.get(User.user_id == user_id)
    history_records = (History
                       .select()
                       .where(
                        (History.user == user) &
                        (fn.DATE(History.search_date) == specified_date)
                        )
                        .order_by(History.search_date.desc()))

    page_count = history_records.count()

    if page_count == 0:
        bot.send_message(message.chat.id, f"Нет запросов за {specified_date}. "
                                          f"Введите новую дату или выберите новую команду")
        return

    paginator = InlineKeyboardPaginator(
        page_count,
        current_page=1,
        data_pattern=f"date_history#{input_date}#{{page}}"
    )

    record = history_records[0]
    result = format_history_record(record)

    bot.send_message(message.chat.id, result, reply_markup=paginator.markup)
    state.delete()