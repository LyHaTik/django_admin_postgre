from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ..db import get_subcategories, get_products, get_cart, put_product_to_cart, get_product
from ..keyboards import get_paginated_ik, get_edit_count_item_ik, get_cart_items_ik
from ..utils import send_product_photo, parse_data
from ..state import CatalogStates, CartStates


# Ловим "category_item:"
async def category_page_handler(callback: CallbackQuery, state: FSMContext):
    category_id, _ = await parse_data(callback.data)
    subcategories = await get_subcategories(category_id=category_id)
    if not subcategories:
        await callback.answer("Нет товаров", show_alert=True)
        return
    
    await state.update_data(categories={}, subcategories=subcategories, cart={})
    await state.set_state(CatalogStates.selecting_subcategory)
    
    await callback.message.edit_text("Выберите подкатегорию:", reply_markup=get_paginated_ik(items=subcategories))

# Ловим "subcategory_item:"
async def subcategory_page_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    subcategory_id, _ = await parse_data(callback.data)
    products = await get_products(subcategory_id=subcategory_id)
    if not products:
        await callback.answer("Нет товаров", show_alert=True)
        return
    
    product = products[0]

    await state.update_data(subcategories={}, products=products)
    await state.set_state(CatalogStates.selecting_product)
    
    await send_product_photo(chat_id=callback.message.chat.id, product=product, products=products)

# Ловим "to_cart", "plus", "minus"
async def cart_add_handler(callback: CallbackQuery, state: FSMContext):
    product_id, quantity = await parse_data(callback.data)
    
    data = await state.get_data()
    cart = data.get("cart", {})
    if quantity is None:
        quantity = cart.get(product_id, 0)
    
    cart[product_id] = quantity
    await state.update_data(cart=cart)
    
    await callback.message.edit_reply_markup(reply_markup=get_edit_count_item_ik(item_id=product_id, count=quantity))

# Ловим "back"
async def cart_back_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    products = data.get("products")
    product = products[0]

    await callback.message.delete()
    await send_product_photo(chat_id=callback.message.chat.id, product=product, products=products)

# Ловим "make_order"
async def make_order_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    user_id = int(callback.from_user.id)
    data = await state.get_data()
    cart = data.get("cart", {})
    if not cart:
        await callback.answer(
            show_alert=True,
            text="🛒 Корзина пуста."
        )
        return

    for product_id, quantity in cart.items():
        await put_product_to_cart(user_id=user_id, product_id=product_id, quantity=quantity)

    cart = await get_cart(user_id)
    
    await state.update_data(cart={})
    await state.set_state(CartStates.viewing_cart)
    
    await callback.message.answer("🛒 Ваша корзина оформлена:\n", reply_markup=get_cart_items_ik(cart))

# Ловим "product_info:"
async def product_info_handler(callback: CallbackQuery):
    product_id, _ = await parse_data(callback.data)
    
    product = await get_product(product_id)
    
    await callback.answer(show_alert=True, text=f'{product.description}')


def register_catalog(dp: Dispatcher):
    dp.callback_query.register(category_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_category))
    dp.callback_query.register(subcategory_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_subcategory))
    dp.callback_query.register(cart_add_handler, F.data.startswith("to_cart:"), StateFilter(CatalogStates.selecting_product))
    dp.callback_query.register(cart_add_handler, F.data.startswith("plus:"), StateFilter(CatalogStates.selecting_product))
    dp.callback_query.register(cart_add_handler, F.data.startswith("minus:"), StateFilter(CatalogStates.selecting_product))
    dp.callback_query.register(cart_back_handler, F.data.startswith("back:"), StateFilter(CatalogStates.selecting_product))
    dp.callback_query.register(make_order_handler, F.data.startswith("make_order:"), StateFilter(CatalogStates.selecting_product))
    dp.callback_query.register(product_info_handler, F.data.startswith("product_info:"), StateFilter(CatalogStates.selecting_product))
