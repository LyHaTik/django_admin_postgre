from aiogram import Bot
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")  # числовой ID
CHANNEL_NAME = os.getenv("CHANNEL_NAME") # формат: channelusername без @
DEFAULT_PER_PAGE=5 # кол-во на странице по умолчанию
PROVIDER_TOKEN = os.getenv('PROVIDER_TOKEN')  # токен ЮКасса
ORDERS_FILE = os.getenv('ORDERS_FILE') # файл сохранения заказов

bot = Bot(BOT_TOKEN)

FAQ_DATA = [
    {"question": "Как выбрать автомобиль?", "answer": "Нажмите Каталог и следуйте по фильтрам кнопок."},
    {"question": "Какие документы нужны для управления автомобилем?", "answer": "Водительские права."},
    {"question": "Как вернуть авто?", "answer": "Напишите нашему администратору @Петрович."},
    {"question": "Можно в Traid-in?", "answer": "Да, через личный кабинет или поддержку."},
    {"question": "Что делать при аварии?", "answer": "Позвоните в поддержку, мы всё оформим."},
]

NEWSLETTER_TEXT = 'Это текст рассылки пользователям Бота.'
