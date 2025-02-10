import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE

def setup_logging():
    rotating_file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=1024**3,  # 1 ГБ
        backupCount=1
    )
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            rotating_file_handler,
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("aiogram")

logger = setup_logging()
