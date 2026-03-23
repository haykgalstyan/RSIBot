import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            RotatingFileHandler(
                Path(__file__).resolve().parent.parent.parent / "bot.log",
                maxBytes=10 * 1024 * 1024,
                backupCount=10,
            ),
            logging.StreamHandler(),
        ],
    )
