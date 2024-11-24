import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler('logs/app.log', maxBytes=5 * 1024 * 1024, backupCount=3)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

logger = logging.getLogger(__name__)
