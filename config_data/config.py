import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_PATH = "database.db"
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("RAPID_API_KEY")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ('hello_world', 'Приветствие бота'),
    ('movie_search', 'Поиск фильма/сериала по названию'),
    ('movie_by_rating', 'Поиск фильмов/сериалов по рейтингу'),
    ('low_budget_movie', 'Поиск фильмов/сериалов с низким бюджетом'),
    ('high_budget_movie', 'Поиск фильмов/сериалов с высоким бюджетом'),
    ("history", "История запросов"),
    ('cancel', 'Обнулить поиск')
)
