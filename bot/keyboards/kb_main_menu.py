from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_rk() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗂 Каталог")],
            [KeyboardButton(text="🗑 Корзина")],
            ],
        resize_keyboard=True
    )


def get_phone_request_rk() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Отправить номер", request_contact=True)]
            ],
        resize_keyboard=True,
        one_time_keyboard=True
    )