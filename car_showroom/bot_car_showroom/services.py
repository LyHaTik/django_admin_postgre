# services.py

from .config import bot


async def broadcast_message(text: str, user_ids: list[int]):
    for telegram_id in user_ids:
        try:
            await bot.send_message(chat_id=telegram_id, text=text)
        except Exception as e:
            print(f"Error sending to {telegram_id}: {e}")
