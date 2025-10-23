
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:144.0) Gecko/20100101 Firefox/144.0"
SCROLLS = 10 # количество скроллов для подгрузки постов
MIN_AGE_HOURS = 3 # минимальный возраст поста в часах
MIN_SCORE = 100 # минимальный рейтинг поста
WAIT_TIME_SECONDS = 3 # время ожидания загрузки страницы и подгрузки новых постов, настройте в зависимости от скорости вашего интернета
SUBREDDIT = "cats" # название сабреддита для парсинга

HEADLESS = False # запускать браузер в фоновом режиме