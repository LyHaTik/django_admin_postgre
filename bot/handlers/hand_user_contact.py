from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from db.db_user import update_user_address, update_user_phone

from state import UserInfoStates
from page.pg_user import phone_ok, address_ok, error_phone


# Ожидаем адрес
async def address_input_handler(message: Message, state: FSMContext):
    address = message.text
    user_id = message.from_user.id

    await update_user_address(user_id, address)
    await state.clear()
    
    await address_ok(message=message)
    

# Ожидаем телефон
async def phone_input_handler(message: Message, state: FSMContext):
    if not message.contact:
        await error_phone(message=message)
        return
    phone = message.contact.phone_number
    user_id = message.from_user.id

    await update_user_phone(user_id, phone)
    await state.clear()
    
    await phone_ok(message=message)


def register_user_contact(dp: Dispatcher):
    dp.message.register(address_input_handler, UserInfoStates.waiting_for_address)
    dp.message.register(phone_input_handler, UserInfoStates.waiting_for_phone)
