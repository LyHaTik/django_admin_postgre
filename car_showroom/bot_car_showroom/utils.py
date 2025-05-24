from aiogram.enums import ChatMemberStatus
from aiogram.types import FSInputFile

from datetime import datetime

from .config import CHANNEL_ID, bot
from .keyboards import get_paginated_ik


async def is_subscribed(user_id) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != ChatMemberStatus.LEFT
    except Exception:
        return False

async def send_car_photo(chat_id, car, cars, page=1):
    photo = FSInputFile(car.image.path)
    caption = f"{car}\nЦена: {car.price}₽"
    keyboard = get_paginated_ik(cars, page=page, per_page=1)
    await bot.send_photo(chat_id, photo, caption=caption, reply_markup=keyboard)

async def parse_data(data: str) -> tuple:
    parts = data.split(":")
    print(f'Parsing: {parts}')
    return int(parts[1]), int(parts[2]) if len(parts) > 2 else None

async def make_order_id() -> int:
    return int(datetime.now().strftime("%Y%m%d%H%M%S"))
