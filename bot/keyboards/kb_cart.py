from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cart_ik(cart: list) -> InlineKeyboardMarkup:
    buttons = []

    for product in cart:
        product_id = product['product_id']
        product_name = product['name']
        quantity = product['quantity']
        buttons.append([
            InlineKeyboardButton(text=f"{product_name}", callback_data="noop"),
            InlineKeyboardButton(text=f"{quantity}", callback_data="noop"),
            InlineKeyboardButton(text="❌", callback_data=f"delete:{product_id}")
        ])

    buttons.append([
        InlineKeyboardButton(text="✅ Оплатить", callback_data="pay:"),
    ])

    return InlineKeyboardMarkup(inline_keyboard=buttons)