from aiogram import F, Dispatcher
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ..db import get_cart, change_quantity_to_cart, delete_item_to_cart, clean_cart, get_user_data_from_db, put_order_id_to_cart
from ..keyboards import get_cart_items_ik
from ..pay import order
from ..state import UserInfoStates, CartStates
from ..utils import parse_data, make_order_id


# Ловим "db_minus", "db_plus:"
async def change_quantity_handler(callback: CallbackQuery):
    user_id = int(callback.from_user.id)
    product_id, quantity = await parse_data(callback.data)

    await change_quantity_to_cart(user_id=user_id, product_id=product_id, quantity=quantity)
    cart = await get_cart(user_id)

    await callback.message.edit_reply_markup(reply_markup=get_cart_items_ik(cart))

# Ловим "db_delete"
async def db_delete_handler(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    product_id, _ = await parse_data(callback.data)

    await delete_item_to_cart(user_id=user_id, product_id=product_id)
    cart = await get_cart(user_id)
    
    if not cart:
        await state.set_state(None)
        
        await callback.message.delete()
        await callback.answer(show_alert=True, text="🛒 Корзина пуста.")
        return

    await callback.message.edit_reply_markup(reply_markup=get_cart_items_ik(cart))

# Ловим "db_clean"
async def db_clean_handler(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    await clean_cart(user_id=user_id)
    
    await state.set_state(None)
    
    await callback.message.delete()
    await callback.answer(show_alert=True, text="🛒 Корзина пуста.")

# Ловим "db_pay"
async def db_pay_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    user = await get_user_data_from_db(user_id)
    address = user.address
    phone = user.phone
    order_id = await make_order_id()
    cart = await get_cart(user_id)
    await put_order_id_to_cart(cart, order_id)

    await callback.message.delete()
    if address and phone:
        await order(chat_id=user_id)
        await state.set_state(None)
    else:
        await callback.message.answer(
            "Перед оплатой, пожалуйста, напишите ваш адрес.",
            reply_markup=None
        )
        await state.set_state(UserInfoStates.waiting_for_address)


def register_cart(dp: Dispatcher):
    dp.callback_query.register(change_quantity_handler, F.data.startswith("db_minus:"), StateFilter(CartStates.viewing_cart))
    dp.callback_query.register(change_quantity_handler, F.data.startswith("db_plus:"), StateFilter(CartStates.viewing_cart))
    dp.callback_query.register(db_delete_handler, F.data.startswith("db_delete:"), StateFilter(CartStates.viewing_cart))
    dp.callback_query.register(db_clean_handler, F.data.startswith("db_clean:"), StateFilter(CartStates.viewing_cart))
    dp.callback_query.register(db_pay_handler, F.data.startswith("db_pay:"), StateFilter(CartStates.viewing_cart))
