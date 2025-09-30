import os

from dotenv import load_dotenv

BASE_URL_HH_RU = "https://api.hh.ru"

load_dotenv()

DB_PARAMS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}
# ID работодателей с hh.ru
LIST_OF_COMPANIES = [
    1740,  # Яндекс
    3529,  # Сбер
    78638,  # Тинькофф
    15478,  # VK
    2180,  # Ozon
    87021,  # Wildberries
    907345,  # Росатом
    39305,  # Газпром
    3127,  # Лукойл
    67611,  # Тензор (Ярославль)
]
