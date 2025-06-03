from aiogram.types import LabeledPrice, Message, CallbackQuery

from config import PROVIDER_TOKEN
from db.db_cart import put_order_id_to_cart
from utils import create_order_id


async def order_page(cart: list, chat_id: int, callback: CallbackQuery):
    await callback.message.delete()
    
    order_id = await create_order_id()
    
    prices = []
    description_lines = []
            
    for item in cart:
        product_id = item['product_id']
        product_name = item['name']
        price = item['price']
        quantity = item['quantity']
        amount = price * quantity
        
        prices.append(
            LabeledPrice(
                label=f"{product_name} x{quantity}",
                amount=amount * 100 # сумма в копейках!
            )
        )
        description_lines.append(f"{product_name} — {quantity}шт — {amount}₽")
        
        await put_order_id_to_cart(user_id=chat_id, product_id=product_id, order_id=order_id)
    
    description = "\n".join(description_lines)

        # Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000

    await callback.bot.send_invoice(
        chat_id=chat_id,    
        title=f'Покупка через Telegram бот(ЮКаssa).\nЗаказ #{order_id}',
        description=description,
        payload=f'order_{order_id}',
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter='product_shop',
    )


async def successful_payment_page(message: Message):
    amount = message.successful_payment.total_amount // 100
    currency = message.successful_payment.currency

    text = (
        f"💵 Спасибо за оплату {amount} {currency}.\n"
        f"📞 Наш менеджер получил заявку и уже набирает ваш номер телефона."
    )
    
    await message.answer(text)

