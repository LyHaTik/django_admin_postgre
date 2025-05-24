from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ..db import get_categories, get_brands
from ..keyboards import get_paginated_ik
from ..utils import send_car_photo, parse_data
from ..state import CatalogStates


# Ловим "category_page:"
async def category_select_handler(callback: CallbackQuery):
    page, _ = await parse_data(callback.data)
    categories = await get_categories()
    await callback.message.edit_reply_markup(reply_markup=get_paginated_ik(items=categories, page=page))

# Ловим "brand_page:"
async def brand_select_handler(callback: CallbackQuery):
    page, _ = await parse_data(callback.data)
    brands = await get_brands()
    await callback.message.edit_reply_markup(reply_markup=get_paginated_ik(items=brands, page=page))

# Ловим "car_page:"
async def car_select_handler(callback: CallbackQuery, state: FSMContext):
    page, _ = await parse_data(callback.data)
    data = await state.get_data()
    cars = data.get("cars")

    if not cars:
        await callback.answer("Список машин пуст")
        return

    car = cars[page - 1]

    await callback.message.delete()
    await send_car_photo(chat_id=callback.message.chat.id, page=page, car=car, cars=cars)


def register_pagination(dp: Dispatcher):
    dp.callback_query.register(category_select_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_category))
    dp.callback_query.register(brand_select_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_brand))
    dp.callback_query.register(car_select_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_car))
