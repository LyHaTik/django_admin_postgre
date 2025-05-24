from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..db import update_user_address, update_user_phone, get_cart, put_order_id_to_cart
from ..keyboards import get_phone_request_kb
from ..pay import order
from ..state import UserInfoStates
from ..utils import make_order_id


# Ожидаем адрес
async def address_input_handler(message: Message, state: FSMContext):
    address = message.text
    user_id = message.from_user.id

    await update_user_address(user_id, address)
    await message.answer("Адрес сохранён ✅\nТеперь, пожалуйста, отправьте ваш номер телефона:", reply_markup=get_phone_request_kb())
    await state.set_state(UserInfoStates.waiting_for_phone)
    print(await state.get_state())

# Ожидаем телефон
async def phone_input_handler(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Пожалуйста, отправьте свой номер через кнопку.", reply_markup=get_phone_request_kb())
        return

    phone = message.contact.phone_number
    user_id = message.from_user.id

    await update_user_phone(user_id, phone)
    
    order_id = await make_order_id()
    cart = await get_cart(user_id)
    await put_order_id_to_cart(cart, order_id)
    
    await order(order_id=order_id, chat_id=user_id, cart=cart)
    await state.set_state(None)
    print(await state.get_state())


def register_user_contact(dp: Dispatcher):
    dp.message.register(address_input_handler, UserInfoStates.waiting_for_address)
    dp.message.register(phone_input_handler, UserInfoStates.waiting_for_phone)
