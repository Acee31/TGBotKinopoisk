from telebot.states import State, StatesGroup

class UserInputInfo(StatesGroup):

    input_movie = State()
    user_select_id = State()
    input_genre = State()
    input_limit = State()
