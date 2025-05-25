from aiogram.enums import ChatMemberStatus
from aiogram.types import FSInputFile

from datetime import datetime

from .config import CHANNEL_ID, bot
from .keyboards import get_paginated_ik
from .models import Product


async def is_subscribed(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != ChatMemberStatus.LEFT
    except Exception:
        return False

async def send_product_photo(chat_id: int, product: Product, products: list[Product], page=1):
    photo = FSInputFile(product.image.path)
    caption = f"{product}\nЦена: {product.price}₽"
    keyboard = get_paginated_ik(products, page=page, per_page=1)
    await bot.send_photo(chat_id, photo, caption=caption, reply_markup=keyboard)

async def parse_data(data: str) -> tuple:
    parts = data.split(":")
    return int(parts[1]), int(parts[2]) if len(parts) > 2 else None

async def make_order_id() -> int:
    return int(datetime.now().strftime("%Y%m%d%H%M%S"))
