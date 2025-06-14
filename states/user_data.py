from telebot.states import State, StatesGroup

class UserInputInfo(StatesGroup):

    input_movie = State()
    user_select_id = State()
    input_genre = State()
    input_limit = State()

    input_type_of_pictures = State()
    input_rating = State()
    input_limit_rating = State()

    input_type_of_pictures_for_budget = State()
    input_low_budget = State()
    input_limit_for_budget = State()

    input_type_of_pictures_for_h_b = State()
    input_high_budget = State()
    input_limit_for_h_b = State()

    waiting_for_date = State()