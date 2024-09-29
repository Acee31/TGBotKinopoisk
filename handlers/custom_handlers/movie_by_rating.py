from telebot.types import Message, CallbackQuery
from telebot.states.sync.context import StateContext
from states.user_data import UserInputInfo
from utils.search_by_rating import search_movie_by_rating
from keyboards.inline.buttons_pictures_types import create_types_button
from keyboards.inline.movie_rating_buttons import create_movie_rating_buttons

from loader import bot


@bot.message_handler(commands=['movie_by_rating'])
def movie_by_rating(message: Message, state: StateContext) -> None:
    types_keyboards = create_types_button()
    state.set(UserInputInfo.input_type_of_pictures)
    bot.send_message(message.chat.id, 'Будем искать фильм или сериал?', reply_markup=types_keyboards)


@bot.callback_query_handler(func=lambda call: call.data in ['movie', 'series', 'cartoon', 'animated_series', 'anime'])
def handle_picture_types(call: CallbackQuery, state: StateContext) -> None:
    picture_type = {
        'movie': 'Фильм',
        'series': 'Сериал',
        'cartoon': 'Мультфильм',
        'animated_series': 'Анимационный сериал',
        'anime': 'Аниме'
    }[call.data]

    state.add_data(input_type_of_pictures=picture_type)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f'Вы выбрали {picture_type}')
    state.set(UserInputInfo.input_rating)
    bot.send_message(call.message.chat.id, 'Какой рейтинг? (Введите число или диапазон рейтингов, например, 7-8)')


@bot.message_handler(state=UserInputInfo.input_rating)
def ask_limit(message: Message, state: StateContext) -> None:
    state.set(UserInputInfo.input_limit_rating)
    state.add_data(input_rating=message.text)
    bot.send_message(message.chat.id, 'Сколько показать результатов?')


@bot.message_handler(state=UserInputInfo.input_limit_rating)
def finish(message: Message, state: StateContext) -> None:
    try:
        limit = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число (например, 2)')
        return

    with state.data() as data:
        type_picture = data['input_type_of_pictures']
        rating = data['input_rating']

        movie_data = search_movie_by_rating(picture_type=type_picture, kp_rating=rating)

        if movie_data:
            data['movie_data'] = movie_data
            keyboard_rating = create_movie_rating_buttons(movie_data, limit)
            bot.send_message(message.chat.id, 'Выберите из списка ниже для более подробной информации',
                             reply_markup=keyboard_rating)

        else:
            bot.send_message(message.chat.id, 'Фильмы/сериалы не найдены или произошла ошибка.\n'
                                              'Пожалуйста, нажмите новую команду чтобы заново начать поиск.')
            state.delete()
