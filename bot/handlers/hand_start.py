import logging

from aiogram import types, Dispatcher, F

from utils import check_subscribed
from db.db_user import check_create_user
from page.pg_user import welcome_page


logger = logging.getLogger(__name__)


# Ловим /start. Проверка подписки и вызов основного меню ReplyKeyboard
async def start_handler(message: types.Message):
    user_id = int(message.from_user.id)
    logger.info(f"User {user_id} called /start")
    
    await message.delete()
    
    user_id = int(message.from_user.id)
    if await check_subscribed(user_id):
        if await check_create_user(user_id):
            text = "Добро пожаловать!"
        else:
            text = "С возвращением!"
        await welcome_page(text=text, message=message)
    else:
        text = "Пожалуйста, подпишитесь на канал: https://t.me/+iYVd93aFJskxOGMy"   
        await welcome_page(text=text, message=message, reply_markup=None)


async def noop_handler(callback: types.CallbackQuery):
    await callback.answer(cache_time=10)


def register_start(dp: Dispatcher):
    dp.message.register(start_handler, F.text == "/start")
    dp.callback_query.register(noop_handler, F.data.startswith("noop"))