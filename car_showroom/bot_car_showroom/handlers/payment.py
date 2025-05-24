from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, PreCheckoutQuery
from aiogram.fsm.context import FSMContext

from datetime import datetime

from ..db import mark_item_as_payed, get_cart
from ..pay import pre_checkout, successful_payment
from ..excel import save


# Проверка готовности товара от продавца
async def handle_pre_checkout_query(query: PreCheckoutQuery, bot: Bot):
    # Отправляем запрос продавцу о готовности товара
    request_saler = await pre_checkout()
    # Если получаем положительный ответ, запускаем следующую функцию
    if request_saler:
        await bot.answer_pre_checkout_query(query.id, ok=True)
    else:
        await bot.answer('Товар не готов. Продавец свяжется с Вами!')

# Когда оплата прошла
async def successful_payment_handler(message: Message, state: FSMContext):
    user_id = message.from_user.id
    cart = await get_cart(user_id)
    payment = message.successful_payment

    # Подготовим данные для записи
    order_data = []
    for item in cart:
        await mark_item_as_payed(item)
        item_name = f'{item.car.brand.name} {item.car.model_name}'
        item_price = item.car.price*item.quantity
        order = [
            item.order_id,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_id,
            item_name,
            item.quantity,
            item_price,  # в рублях
            payment.currency,
            payment.invoice_payload
            ]
        order_data.append(order)
    
    await save(order_data)
    await state.update_data(cart={})
    await successful_payment(message)


def register_payment(dp: Dispatcher):
    dp.message.register(successful_payment_handler, F.successful_payment)
    dp.pre_checkout_query.register(handle_pre_checkout_query, F.total_amount >= 0)

    