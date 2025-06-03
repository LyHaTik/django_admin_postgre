import logging

from aiogram import F, Dispatcher
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from state import CartStates, CatalogStates
from utils import parse_data
from db.db_cart import put_product_to_cart, delete_product_in_cart
from page.pg_cart import cart_page


logger = logging.getLogger(__name__)


# Ловим "Корзина"
async def show_cart_handler(message: Message, state: FSMContext):
    user_id = int(message.from_user.id)
    await state.set_state(CartStates.viewing_cart)
    
    logger.info(f"User {user_id} opened cart")

    await cart_page(user_id=user_id, state=state, message_or_callback=message)


# Ловим "submit:"
async def submit_cart_handler(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id)
    data = await state.get_data()
    cart = data.get("cart", {})
    
    logger.info(f"User {user_id} submitting cart with items: {cart}")

    for product_id, quantity in cart.items():
        await put_product_to_cart(user_id=user_id, product_id=product_id, quantity=quantity)

    await state.update_data(cart={})
    await state.set_state(CartStates.viewing_cart)

    await cart_page(user_id=user_id, state=state, message_or_callback=callback)
    

# Ловим "delete:"
async def delete_handler(callback: CallbackQuery, state: FSMContext):
    product_id, _ = await parse_data(callback.data)
    user_id = int(callback.from_user.id)
    
    logger.info(f"User {user_id} deleting product {product_id} from cart")
    
    await delete_product_in_cart(user_id=user_id, product_id=product_id)
    await cart_page(user_id=user_id, state=state, message_or_callback=callback)


def register_cart(dp: Dispatcher):
    dp.message.register(show_cart_handler, F.text == "🗑 Корзина")
    dp.callback_query.register(submit_cart_handler, F.data.startswith("submit:"), StateFilter(CatalogStates.selecting_product_quantity))
    dp.callback_query.register(delete_handler, F.data.startswith("delete:"), StateFilter(CartStates.viewing_cart))
