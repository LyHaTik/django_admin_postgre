from aiogram import types, Dispatcher, F
from aiogram.fsm.context import FSMContext

from ..keyboards import main_menu_kb
from ..utils import is_subscribed
from ..db import create_user
from ..config import CHANNEL_NAME


# Ловим /start. Проверка подписки и вызов основного меню ReplyKeyboard
async def start_handler(message: types.Message, state: FSMContext):
    await message.delete()
    user_id = int(message.from_user.id)
    if await is_subscribed(user_id):
        created = await create_user(user_id)
        if created:
            text = "Добро пожаловать!"
        else:
            text = "С возвращением!"
        await message.answer(text, reply_markup=main_menu_kb())
        await state.update_data(cart={})
    else:
        invite_link = f"https://t.me/{CHANNEL_NAME.lstrip('@')}"
        await message.answer(f"Пожалуйста, подпишитесь на канал: https://t.me/+iYVd93aFJskxOGMy")


def register_start(dp: Dispatcher):
    dp.message.register(start_handler, F.text == "/start")