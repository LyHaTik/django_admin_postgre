import asyncio
from aiohttp import web
import logging_config
import logging

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from http_server import app
from handlers import register_all_handlers
from config import bot


logger = logging.getLogger(__name__)


dp = Dispatcher(storage=MemoryStorage())
register_all_handlers(dp)


async def main():
    logger.info("Starting bot...")
    await bot.delete_webhook(drop_pending_updates=True)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8001)
    await site.start()
    logger.info("HTTP server started on port 8001")

    await dp.start_polling(bot, skip_updates=False)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped manually")
    except Exception as e:
        logger.exception("Unexpected error occurred", exc_info=e)
