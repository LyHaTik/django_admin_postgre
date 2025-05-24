import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .handlers import register_all_handlers
from .config import bot


async def main():

    dp = Dispatcher(storage=MemoryStorage())
    register_all_handlers(dp)
    await dp.start_polling(bot, skip_updates=False)

if __name__ == "__main__":
    asyncio.run(main())