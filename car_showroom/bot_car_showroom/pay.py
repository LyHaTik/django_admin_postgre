from aiogram.types import LabeledPrice, Message

from .config import PROVIDER_TOKEN, bot
from .db import get_cart


async def order(chat_id: int):
    cart = await get_cart(user_id=chat_id)
    prices = []
    description = ''
    for item in cart:
        prices.append(
            LabeledPrice(
                label=str(item.product),
                amount=int(item.product.price * 100)*item.quantity  # сумма в копейках!
            )
        )
        description += f'{str(item.product)} {item.quantity}шт \n'
        order_id = item.order_id

    await bot.send_message(
        chat_id=chat_id,
        text='🤖💬: _- рекомендую сохранить данные карты для последующего ввода_\n \
        \n \
        Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000',
        parse_mode="Markdown"
        )
    await bot.send_invoice(
        chat_id=chat_id,    
        title=f'Покупка через Telegram бот(ЮКаssa).\nЗаказ #{order_id}',
        description=description,
        payload='Payment through a bot',
        provider_token=PROVIDER_TOKEN,
        currency="RUB",
        prices=prices,
        start_parameter='product_shop',
    )

async def successful_payment(message: Message):
    msg = f'💵 Спасибо за оплату {message.successful_payment.total_amount // 100} {message.successful_payment.currency}.' \
        f'\r\n - Наш менеджер полчил заявку и уже набирает Ваш номер телефона.'
    # Сообщение продавцу об оплате продукта.
    await message.answer(msg)

async def pre_checkout():
    # Отправляем запрос продавцу о готовности товара
    # Если получаем положительный ответ, запускаем следующую функцию
    return True
