import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PreCheckoutQuery, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from datetime import datetime

from db.db_cart import update_item_as_payed, get_cart
from db.db_user import get_user
from page.pg_payment import successful_payment_page, order_page
from page.pg_user import send_address, send_phone
from utils import save_to_excel
from state import CartStates, UserInfoStates


logger = logging.getLogger(__name__)


# Ловим "pay:"
async def pay_handler(callback: CallbackQuery, state: FSMContext):
    user_id = int(callback.from_user.id) 
    
    logger.info(f"User {user_id} initiated payment.")
    
    user = await get_user(user_id)
    cart = await get_cart(user_id=user_id)
    address = user['address']
    phone = user['phone']

    await state.clear()
    
    if not address:
        logger.info(f"User {user_id} missing address, requesting address.")
        
        await state.set_state(UserInfoStates.waiting_for_address) 
        await send_address(callback=callback)
        return
    if not phone:
        logger.info(f"User {user_id} missing phone, requesting phone.")
        
        await state.set_state(UserInfoStates.waiting_for_phone) 
        await send_phone(callback=callback)
        return
    else:
        logger.info(f"User {user_id} has all data, showing order page.")
        
        await order_page(cart=cart, chat_id=user_id, callback=callback)
        

async def handle_pre_checkout_query(query: PreCheckoutQuery, bot: Bot):
    logger.info(f"PreCheckoutQuery received from user {query.from_user.id} for total_amount={query.total_amount}")
    
    # Отправляем запрос продавцу о готовности товара
    request_saler = True
    # Если получаем положительный ответ, запускаем следующую функцию
    if request_saler:
        await bot.answer_pre_checkout_query(query.id, ok=True)
        logger.info(f"PreCheckoutQuery accepted for user {query.from_user.id}")
    else:
        await bot.answer('Товар не готов. Продавец свяжется с Вами!')
        logger.warning(f"PreCheckoutQuery rejected for user {query.from_user.id}: товар не готов")


async def successful_payment_handler(message: Message):
    user_id = message.from_user.id
    
    logger.info(f"Successful payment from user {user_id}")
    
    cart = await get_cart(user_id)
    payment = message.successful_payment

    await update_item_as_payed(user_id)

    order_data = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    for item in cart:
        order_data.append({
            "Order ID": item['order_id'],
            "Дата": timestamp,
            "User ID": user_id,
            "Товар": item['name'],
            "Кол-во": item['quantity'],
            "Сумма": item['price'],
            "Валюта": payment.currency,
            "Описание": payment.invoice_payload
        })
    
    await save_to_excel(order_data)
    await successful_payment_page(message)
    logger.info(f"Payment processed and saved for user {user_id}")


def register_payment(dp: Dispatcher):
    dp.callback_query.register(pay_handler, F.data.startswith("pay:"), StateFilter(CartStates.viewing_cart))
    dp.message.register(successful_payment_handler, F.successful_payment)
    dp.pre_checkout_query.register(handle_pre_checkout_query, F.total_amount >= 0)

    