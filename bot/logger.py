"""Logging configuration for the bot."""

import logging
import logging.handlers
from pathlib import Path
from pythonjsonlogger import jsonlogger
from bot.config import config


def setup_logging() -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger("obfbot")
    logger.setLevel(getattr(logging, config.LOG_LEVEL))

    # Create logs directory
    Path("logs").mkdir(exist_ok=True)

    # File handler with JSON formatting
    fh = logging.handlers.RotatingFileHandler(
        config.LOG_FILE,
        maxBytes=10_000_000,  # 10MB
        backupCount=5,
    )
    fh.setLevel(logging.DEBUG)
    fh_formatter = jsonlogger.JsonFormatter()
    fh.setFormatter(fh_formatter)
    logger.addHandler(fh)

    # Console handler with standard formatting
    ch = logging.StreamHandler()
    ch.setLevel(getattr(logging, config.LOG_LEVEL))
    ch_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(ch_formatter)
    logger.addHandler(ch)

    return logger


logger = setup_logging()
