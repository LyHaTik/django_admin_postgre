from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..db import update_user_address, update_user_phone
from ..keyboards import get_phone_request_kb
from ..pay import order
from ..state import UserInfoStates


# Ожидаем адрес
async def address_input_handler(message: Message, state: FSMContext):
    address = message.text
    user_id = message.from_user.id

    await update_user_address(user_id, address)
    await state.set_state(UserInfoStates.waiting_for_phone)
    
    await message.answer("Адрес сохранён ✅\nТеперь, пожалуйста, отправьте ваш номер телефона:", reply_markup=get_phone_request_kb())

# Ожидаем телефон
async def phone_input_handler(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Пожалуйста, отправьте свой номер через кнопку.", reply_markup=get_phone_request_kb())
        return
    phone = message.contact.phone_number
    user_id = message.from_user.id

    await update_user_phone(user_id, phone)
    
    await order(chat_id=user_id)
    await state.set_state(None)


def register_user_contact(dp: Dispatcher):
    dp.message.register(address_input_handler, UserInfoStates.waiting_for_address)
    dp.message.register(phone_input_handler, UserInfoStates.waiting_for_phone)
