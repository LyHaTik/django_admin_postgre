from aiogram import Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from ..db import get_categories, get_cart
from ..keyboards import get_paginated_ik, get_cart_items_ik
from ..state import CatalogStates, CartStates


# Ловим "Каталог". 
async def catalog_handler_message(message: Message, state: FSMContext):
    await message.delete()
    categories = await get_categories()
    await message.answer("Выберите категорию:", reply_markup=get_paginated_ik(items=categories))
    
    await state.update_data(cart={})
    await state.set_state(CatalogStates.selecting_category)
    print(await state.get_state())

# Ловим "Корзина".
async def cart_handler_message(message: Message, state: FSMContext):
    await message.delete()
    user_id = int(message.from_user.id)
    cart = await get_cart(user_id)
    if not cart:
        await message.answer("🛒 Ваша корзина пуста.")
        await state.clear()
        return
    text = "Ваша Корзина:"
    
    await message.answer(text, reply_markup=get_cart_items_ik(cart))
    
    await state.set_state(CartStates.viewing_cart)
    print(await state.get_state())
    await state.update_data(cart=cart)


def register_main_menu(dp: Dispatcher):
    dp.message.register(cart_handler_message, F.text == "🗑 Корзина")
    dp.message.register(catalog_handler_message, F.text == "🗂 Каталог")