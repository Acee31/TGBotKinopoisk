from telebot.types import Message, CallbackQuery
from telebot import custom_filters
from telebot.states.sync.context import StateContext
from states.user_data import UserInputInfo
from utils.search_movie_by_name import search_movie_by_name_a_genre
from keyboards.inline.movie_buttons import create_movie_buttons
from keyboards.inline.buttons_yes_no_on_genre import create_yes_no_keyboard
from handlers.custom_handlers.callback.callback_send_movie_info import send_movie_info
from loader import bot


@bot.message_handler(commands=['movie_search'])
def movie_search(message: Message, state: StateContext) -> None:
    state.set(UserInputInfo.input_movie)
    bot.send_message(message.chat.id, 'Введите фильм/сериал (введите на русском)')


@bot.message_handler(state='*', commands=['cancel'])
def any_state(message: Message, state: StateContext) -> None:
    state.delete()
    bot.send_message(message.chat.id, 'Ваша информация удалена. Нажмите /start чтобы начать.')


@bot.message_handler(state=UserInputInfo.input_movie)
def movie_name_get(message: Message, state: StateContext) -> None:
    state.set(UserInputInfo.input_genre)
    state.add_data(input_movie=message.text)
    keyboard_yes_no = create_yes_no_keyboard()
    bot.send_message(
        message.chat.id,
        'Хотите уточнить жанр?',
        reply_markup=keyboard_yes_no
    )


@bot.callback_query_handler(func=lambda call: call.data == 'yes_genre')
def ask_genre(call: CallbackQuery, state: StateContext) -> None:
    state.set(UserInputInfo.input_genre)
    bot.send_message(call.message.chat.id, 'Какой жанр? (введите на русском)')


@bot.message_handler(state=UserInputInfo.input_genre)
def genre_name_get(message: Message, state: StateContext) -> None:
    state.set(UserInputInfo.input_limit)
    state.add_data(input_genre=message.text)
    bot.send_message(message.chat.id, 'Сколько показать результатов? (введите число)')


@bot.callback_query_handler(func=lambda call: call.data == 'no_genre')
def ask_limit(call: CallbackQuery, state: StateContext) -> None:
    state.set(UserInputInfo.input_limit)
    bot.send_message(call.message.chat.id, 'Сколько показать результатов? (введите число)')


@bot.message_handler(state=UserInputInfo.input_limit)
def finish(message: Message, state: StateContext) -> None:
    try:
        limit = int(message.text)
    except ValueError:
        bot.send_message(message.chat.id, 'Пожалуйста, введите корректное число (например, 2)')
        return

    with state.data() as data:
        movie_name = data.get('input_movie')
        genre = data.get('input_genre', None)

        movie_data = search_movie_by_name_a_genre(movie_name=movie_name, genre=genre)
        if movie_data:
            data['movie_data'] = movie_data
            keyboard = create_movie_buttons(movie_data, limit)
            bot.send_message(message.chat.id, 'Выберите из списка ниже для более подробной информации',
                             reply_markup=keyboard)
            send_movie_info()
        else:
            bot.send_message(message.chat.id, 'Фильмы/сериалы не найдены или произошла ошибка.\n'
                                              'Пожалуйста, нажмите /movie_search, чтобы заново начать поиск.')
            state.delete()


bot.add_custom_filter(custom_filters.StateFilter(bot))
from telebot.states.sync.middleware import StateMiddleware

bot.setup_middleware(StateMiddleware(bot))