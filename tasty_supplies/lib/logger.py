import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[34m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
    }
    RESET = "\033[0m"

    def format(self, record):
        levelname = record.levelname
        message = super().format(record)
        color = self.COLORS.get(levelname, "")
        return f"{color}{message}{self.RESET}"


def get_logger(name="ts_logger"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    handler = logging.StreamHandler()
    formatter = ColoredFormatter(" %(levelname)7s | %(message)s")
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    logger.propagate = False

    return logger


log = get_logger()
