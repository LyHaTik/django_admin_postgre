from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from ..keyboards import get_paginated_ik
from ..utils import send_product_photo, parse_data
from ..state import CatalogStates


# Ловим "category_page:"
async def category_select_handler(callback: CallbackQuery, state: FSMContext):
    page, _ = await parse_data(callback.data)
    data = await state.get_data()
    categories = data.get("categories")

    if not categories:
        await callback.answer("Список подкатегорий пуст")
        return
    await callback.message.edit_reply_markup(reply_markup=get_paginated_ik(items=categories, page=page))

# Ловим "subcategory_page:"
async def subcategory_select_handler(callback: CallbackQuery, state: FSMContext):
    page, _ = await parse_data(callback.data)
    data = await state.get_data()
    subcategories = data.get("subcategories")

    if not subcategories:
        await callback.answer("Список подкатегорий пуст")
        return
    await callback.message.edit_reply_markup(reply_markup=get_paginated_ik(items=subcategories, page=page))

# Ловим "product_page:"
async def product_select_handler(callback: CallbackQuery, state: FSMContext):
    page, _ = await parse_data(callback.data)
    data = await state.get_data()
    products = data.get("products")

    if not products:
        await callback.answer("Список машин пуст")
        return

    product = products[page - 1]

    await callback.message.delete()
    await send_product_photo(chat_id=callback.message.chat.id, page=page, product=product, products=products)


def register_pagination(dp: Dispatcher):
    dp.callback_query.register(category_select_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_category))
    dp.callback_query.register(subcategory_select_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_subcategory))
    dp.callback_query.register(product_select_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_product))
