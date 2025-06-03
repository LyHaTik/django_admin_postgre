import logging

from aiogram import Dispatcher, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from db.db_catalog import get_categories, get_subcategories, get_products
from utils import parse_data
from state import CatalogStates
from keyboards.kb_catalog import paginated_ik
from page.pg_catalog import categories_page, subcategories_page, products_page, product_page


logger = logging.getLogger(__name__)


# Ловим "Каталог"
async def catalog_handler_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"User {user_id} opened catalog")
    
    categories = await get_categories()
    await state.update_data(categories=categories)
    await state.set_state(CatalogStates.selecting_category)

    await categories_page(message=message, state=state)


# Ловим "item:" "state.CatalogStates.selecting_category"
async def category_page_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    category_id, _ = await parse_data(callback.data)
    logger.info(f"User {user_id} selected category {category_id}")
    
    subcategories = await get_subcategories(category_id=category_id)
    await state.update_data(subcategories=subcategories)
    await state.set_state(CatalogStates.selecting_subcategory)
    await subcategories_page(callback=callback, state=state)


# Ловим "item:" "state.CatalogStates.selecting_subcategory"
async def subcategory_page_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    subcategory_id, _ = await parse_data(callback.data)
    logger.info(f"User {user_id} selected subcategory {subcategory_id}")
    
    products = await get_products(subcategory_id=subcategory_id)
    await state.update_data(products=products)
    await state.set_state(CatalogStates.selecting_product)
    await products_page(callback=callback, state=state)


# Ловим "item:" "CatalogStates.selecting_product"
async def product_page_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    product_id, _ = await parse_data(callback.data)
    logger.info(f"User {user_id} viewed product {product_id}")

    data = await state.get_data()
    cart = data.get("cart", {})
    cart[product_id] = 1
    await state.update_data(cart=cart)
    await state.set_state(CatalogStates.selecting_product_quantity)

    await product_page(callback=callback, product_id=product_id, quantity=cart[product_id])
    

# Ловим "item:" "CatalogStates.selecting_product_quantity"
async def product_quantity_page_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    product_id, plus_or_minus = await parse_data(callback.data)
    logger.info(f"User {user_id} changed quantity for product {product_id} by '{plus_or_minus}'")
    
    data = await state.get_data()
    cart = data.get("cart", {})

    if plus_or_minus == "+":
        cart[product_id] += 1
    elif plus_or_minus == "-":
        cart[product_id] -= 1
    await state.update_data(cart=cart)

    await product_page(callback=callback, product_id=product_id, quantity=cart[product_id])


# Ловим "page:" "CatalogStates.selecting_category"
async def category_pagination_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    page, _ = await parse_data(callback.data)
    logger.info(f"User {user_id} paginated categories to page {page}")
    
    data = await state.get_data()
    categories = data.get('categories')
    reply_markup = await paginated_ik(items=categories, page=page)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


# Ловим "page:" "CatalogStates.selecting_subcategory"
async def subcategory_pagination_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    page, _ = await parse_data(callback.data)
    logger.info(f"User {user_id} paginated subcategories to page {page}")
    
    data = await state.get_data()
    subcategories = data.get('subcategories')
    reply_markup = await paginated_ik(items=subcategories, page=page)
    await callback.message.edit_reply_markup(reply_markup=reply_markup)


# Ловим "page:" "CatalogStates.selecting_product"
async def product_pagination_handler(callback: CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    page, _ = await parse_data(callback.data)
    logger.info(f"User {user_id} paginated products to page {page}")
    
    await products_page(callback=callback, state=state, page=page)


def register_catalog(dp: Dispatcher):
    dp.message.register(catalog_handler_message, F.text == "🗂 Каталог")
    dp.callback_query.register(category_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_category))
    dp.callback_query.register(subcategory_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_subcategory))
    dp.callback_query.register(product_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_product))
    dp.callback_query.register(product_quantity_page_handler, F.data.startswith("item:"), StateFilter(CatalogStates.selecting_product_quantity))
    dp.callback_query.register(category_pagination_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_category))
    dp.callback_query.register(subcategory_pagination_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_subcategory))
    dp.callback_query.register(product_pagination_handler, F.data.startswith("page:"), StateFilter(CatalogStates.selecting_product))