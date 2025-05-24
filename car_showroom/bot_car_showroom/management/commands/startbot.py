from django.core.management.base import BaseCommand
import asyncio

from ...bot import main as bot_main


class Command(BaseCommand):
    help = 'Telegram bot "TEST_CAS_SHOWROOM"'
    
    def handle(self, *args, **options):
        self.stdout.write("Бот запущен...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(bot_main())
        except KeyboardInterrupt:
            self.stdout.write("Бот остановлен.")
        finally:
            loop.close()