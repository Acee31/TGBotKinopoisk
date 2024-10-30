from datetime import datetime
from loader import bot
from telebot.types import CallbackQuery
from telebot.states.sync.context import StateContext
from database.models import User, History


@bot.callback_query_handler(func=lambda call: call.data.startswith('movie_'))
def send_movie_info(call: CallbackQuery, state: StateContext) -> None:
    movie_index = int(call.data.split('_')[1])

    with bot.retrieve_data(call.message.chat.id) as data:
        movie_data = data.get('movie_data')

    if movie_data and movie_index < len(movie_data):
        movie = movie_data[movie_index]

        title = movie.get('name', 'Неизвестно')
        description = movie.get('description', 'Нет описания')
        rating = movie.get('rating', {}).get('kp', 'Нет рейтинга')
        year = movie.get('year', 'Неизвестно')
        movie_genres = ', '.join([genre['name'] for genre in movie['genres']])
        adult_rating = movie.get('ratingMpaa', 'Неизвестно')
        poster = movie.get('poster', {}).get('url', 'Неизвестно')

        msg = (
            f'Название: {title}\n'
            f'Описание: {description}\n'
            f'Рейтинг: {rating}\n'
            f'Год производства: {year}\n'
            f'Жанр: {movie_genres}\n'
            f'Возрастной рейтинг: {adult_rating}\n'
            f'Постер: {poster}'
        )

        bot.send_message(call.message.chat.id, msg)

        user = User.get(User.user_id == call.from_user.id)
        History.create(
            user=user,
            search_date=datetime.now(),
            title=title,
            description=description,
            rating=rating,
            year=year,
            genre=movie_genres,
            adult_rating=adult_rating,
            poster=poster
        )

    else:
        bot.send_message(call.message.chat.id, 'Информация о фильме не найдена.')

    state.delete()
    bot.send_message(call.message.chat.id, 'Ваше состояние очищено.\nВыберете новою команду.')