"""Logging configuration for Tasty Supplies.

This module provides colored console logging with customizable formatting.
"""

import logging
from typing import Dict


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds ANSI color codes to log messages."""

    COLORS: Dict[str, str] = {
        "DEBUG": "\033[34m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET: str = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with color based on its level.

        Args:
            record: The log record to format

        Returns:
            Formatted and colored log message
        """
        levelname: str = record.levelname
        message: str = super().format(record)
        color: str = self.COLORS.get(levelname, "")
        return f"{color}{message}{self.RESET}"


def get_logger(name: str = "ts_logger") -> logging.Logger:
    """Get or create a configured logger instance.

    Args:
        name: Name for the logger instance

    Returns:
        Configured logger with colored console output
    """
    logger: logging.Logger = logging.getLogger(name)
    logger.setLevel(level=logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler: logging.StreamHandler = logging.StreamHandler()
    formatter: ColoredFormatter = ColoredFormatter(" %(levelname)7s | %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False

    return logger


log: logging.Logger = get_logger()
