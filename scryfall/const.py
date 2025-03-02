import logging

__version__ = "0.1.1"

logger_name = "scryfall"

_logger = logging.getLogger(logger_name)


def get_logger() -> logging.Logger:
    global _logger
    return _logger
