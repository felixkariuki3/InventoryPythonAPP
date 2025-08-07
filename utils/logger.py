import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    # Ensure logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    log_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    log_file = "logs/app.log"
    file_handler = RotatingFileHandler(
        log_file, maxBytes=5 * 1024 * 1024, backupCount=2
    )
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.DEBUG)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # Avoid duplicate handlers on reload
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
