from datetime import datetime
from peewee import fn
from loader import bot
from telegram_bot_pagination import InlineKeyboardPaginator
from database.models import User, History
from telebot.types import CallbackQuery


@bot.callback_query_handler(func=lambda call: call.data.startswith("history#"))
def handle_pagination(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    page = int(call.data.split("#")[1])

    user = User.get(User.user_id == user_id)
    history_records = History.select().where(History.user == user).order_by(History.search_date.desc())

    if page > history_records.count():
        bot.answer_callback_query(call.id, "Запрошенная страница отсутствует.")
        return

    record = history_records[page - 1]
    result = format_history_record(record)

    paginator = InlineKeyboardPaginator(
        history_records.count(),
        current_page=page,
        data_pattern="history#{page}"
    )

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result,
                          reply_markup=paginator.markup)
    bot.answer_callback_query(call.id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("date_history#"))
def handle_date_pagination(call: CallbackQuery) -> None:
    user_id = call.from_user.id
    data = call.data.split("#")
    input_date = data[1]
    page = int(data[2])

    user = User.get(User.user_id == user_id)
    specified_date = datetime.strptime(input_date, "%Y-%m-%d").date()

    history_records = (History
                       .select()
                       .where(
        (History.user == user) &
        (fn.DATE(History.search_date) == specified_date)
    )
                       .order_by(History.search_date.desc()))

    if page > history_records.count():
        bot.answer_callback_query(call.id, "Запрошенная страница отсутствует.")
        return

    record = history_records[page - 1]
    result = format_history_record(record)

    paginator = InlineKeyboardPaginator(
        history_records.count(),
        current_page=page,
        data_pattern=f"date_history#{input_date}#{{page}}"
    )

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result,
                          reply_markup=paginator.markup)
    bot.answer_callback_query(call.id)


def format_history_record(record: History) -> str:
    return (
        f"Дата: {record.search_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Название: {record.title}\n"
        f"Описание: {record.description}\n"
        f"Рейтинг: {record.rating}\n"
        f"Год производства: {record.year}\n"
        f"Жанр: {record.genre}\n"
        f"Возрастной рейтинг: {record.adult_rating}\n"
        f"Постер: {record.poster}"
    )
