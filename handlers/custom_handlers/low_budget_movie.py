from telebot.types import Message, CallbackQuery
from telebot.states.sync.context import StateContext
from states.user_data import UserInputInfo
from keyboards.inline.buttons_pictures_types_low_budget import create_types_button_for_budget
from utils.search_movie_with_low_budget import search_movie_by_low_budget
from keyboards.inline.buttons_picture_low_budget import create_movie_budget_buttons
from database.models import User
from loader import bot


@bot.message_handler(commands=["low_budget_movie"])
def low_budget_movie(message: Message, state: StateContext) -> None:
    user_id = message.from_user.id
    if User.get_or_none(User.user_id == user_id) is None:
        bot.reply_to(message, "Вы не зарегистрированы. Выполните команду /start")
        return

    types_keyboards = create_types_button_for_budget()
    state.set(UserInputInfo.input_type_of_pictures_for_budget)
    bot.send_message(message.chat.id, 'Будем искать фильм или сериал?', reply_markup=types_keyboards)


@bot.callback_query_handler(func=lambda call: call.data in ['budget_movie', 'budget_series', 'budget_cartoon', 'budget_animated_series', 'budget_anime'])
def handle_budget_picture_types(call: CallbackQuery, state: StateContext) -> None:
    picture_type = {
        'budget_movie': 'Фильм',
        'budget_series': 'Сериал',
        'budget_cartoon': 'Мультфильм',
        'budget_animated_series': 'Анимационный сериал',
        'budget_anime': 'Аниме'
    }[call.data]

    state.add_data(input_type_of_pictures_for_budget=picture_type)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Вы выбрали {picture_type}')
    state.set(UserInputInfo.input_low_budget)
    bot.send_message(call.message.chat.id, 'Какой бюджет?')


@bot.message_handler(state=UserInputInfo.input_low_budget)
def ask_limit(message: Message, state: StateContext) -> None:
    try:
        low_budget_info = int(message.text)
        state.add_data(input_low_budget=low_budget_info)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число (например, 10000)')
        return
    state.set(UserInputInfo.input_limit_for_budget)
    bot.send_message(message.chat.id, 'Сколько показать результатов?')


@bot.message_handler(state=UserInputInfo.input_limit_for_budget)
def finish(message: Message, state: StateContext) -> None:
    try:
        limit = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число (например, 2)')
        return

    with state.data() as data:
        type_picture_budget = data['input_type_of_pictures_for_budget']
        low_budget = data['input_low_budget']

        movie_data = search_movie_by_low_budget(picture_type=type_picture_budget, curr=low_budget)
        if movie_data:
            data['movie_data'] = movie_data
            keyboard_low_budget = create_movie_budget_buttons(movie_data, limit)
            bot.send_message(message.chat.id, 'Выберите из списка ниже для более подробной информации',
                             reply_markup=keyboard_low_budget)

        else:
            bot.send_message(message.chat.id, 'Фильмы/сериалы не найдены или произошла ошибка.\n'
                                              'Пожалуйста, нажмите новую команду чтобы заново начать поиск.')
            state.delete()





