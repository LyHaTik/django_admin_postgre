from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ..db import get_brands, get_cars, get_cart, put_car_to_cart, get_car
from ..keyboards import get_paginated_ik, get_edit_count_item_ik, get_cart_items_ik
from ..utils import send_car_photo, parse_data
from ..state import CatalogStates, CartStates


# Ловим "category_item:"
async def category_page_handler(callback: CallbackQuery, state: FSMContext):
    category_id, _ = await parse_data(callback.data)
    await state.update_data(selected_category_id=category_id)
    await state.set_state(CatalogStates.selecting_brand)
    print(await state.get_state())
    
    brands = await get_brands()
    await callback.message.edit_text("Выберите марку:", reply_markup=get_paginated_ik(items=brands))


# Ловим "brand_item:"
async def brand_page_handler(callback: CallbackQuery, state: FSMContext):
    brand_id, _ = await parse_data(callback.data)
    data = await state.get_data()
    category_id = data.get("selected_category_id")
    
    cars = await get_cars(category_id=category_id, brand_id=brand_id)
    if not cars:
        await callback.answer("Нет машин этой марки", show_alert=True)
        return
    car = cars[0]

    await state.update_data(cars=cars)
    await state.set_state(CatalogStates.selecting_car)
    print(await state.get_state())
    
    await callback.message.delete()
    await send_car_photo(chat_id=callback.message.chat.id, car=car, cars=cars)


### Хэндлеры корзины в state
# Ловим "to_cart", "plus", "minus"
async def cart_add_handler(callback: CallbackQuery, state: FSMContext):
    car_id, quantity = await parse_data(callback.data)
    data = await state.get_data()
    cart = data.get("cart", {})
    if quantity is None:
        quantity = cart.get(car_id, 0)
    
    cart[car_id] = quantity
    
    await state.update_data(cart=cart)

    await callback.message.edit_reply_markup(reply_markup=get_edit_count_item_ik(item_id=car_id, count=quantity))

# Ловим "back"
async def cart_back_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    cars = data.get("cars")
    car = cars[0]

    await callback.message.delete()
    await send_car_photo(chat_id=callback.message.chat.id, car=car, cars=cars)

# Ловим "make_order"
async def make_order_handler(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    data = await state.get_data()
    cart = data.get("cart", {})

    await callback.message.delete()
    if not cart:
        await callback.answer(
            show_alert=True,
            text="🛒 Корзина пуста."
        )
        return

    text = "🛒 Ваша корзина оформлена:\n"
    for car_id, quantity in cart.items():
        await put_car_to_cart(user_id=user_id, car_id=car_id, quantity=quantity)  # Функция, сохраняющая в БД

    cart = await get_cart(user_id)
    await state.update_data(cart=cart)
    await state.set_state(CartStates.viewing_cart)
    print(await state.get_state())
    
    await callback.message.answer(text, reply_markup=get_cart_items_ik(cart))


# Ловим "car_info:"
async def car_info_handler(callback: CallbackQuery):
    car_id, _ = await parse_data(callback.data)
    car = await get_car(car_id)
    await callback.answer(
        show_alert=True,
        text=f'Год: {car.year}г\nПробег: {car.mileage}(км)\n{car.description}'
    )


def register_catalog(dp: Dispatcher):
    dp.callback_query.register(category_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_category))
    dp.callback_query.register(brand_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_brand))
    dp.callback_query.register(cart_add_handler, F.data.startswith("to_cart:"), StateFilter(CatalogStates.selecting_car))
    dp.callback_query.register(cart_add_handler, F.data.startswith("plus:"), StateFilter(CatalogStates.selecting_car))
    dp.callback_query.register(cart_add_handler, F.data.startswith("minus:"), StateFilter(CatalogStates.selecting_car))
    dp.callback_query.register(cart_back_handler, F.data.startswith("back:"), StateFilter(CatalogStates.selecting_car))
    dp.callback_query.register(make_order_handler, F.data.startswith("make_order:"), StateFilter(CatalogStates.selecting_car))
    dp.callback_query.register(car_info_handler, F.data.startswith("car_info:"), StateFilter(CatalogStates.selecting_car))
