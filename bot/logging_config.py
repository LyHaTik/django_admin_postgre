import logging
from logging.handlers import RotatingFileHandler
import os


LOG_DIR = "shared_media"
LOG_FILE = "bot_logs.log"
os.makedirs(LOG_DIR, exist_ok=True)


rotating_handler = RotatingFileHandler(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    maxBytes=5 * 1024 * 1024,
    backupCount=3,             
    encoding='utf-8'
)


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
rotating_handler.setFormatter(formatter)


logging.basicConfig(
    level=logging.INFO,
    handlers=[rotating_handler, logging.StreamHandler()]
)