"""Logging setup for the server."""

import logging
import sys

LOG_FORMAT = "[%(asctime)s] %(levelname)s [%(module)s]: %(message)s"
LOG_DATE_FORMAT = "%d/%m/%Y | %H:%M:%S"
LOG_LEVEL = "INFO"


def setup_logging() -> None:
    """Configure logging with both console and rotating file handlers.

    Creates a logs directory if it doesn't exist and sets up:
    - Console handler for stdout
    - Rotating file handler with size-based rotation
    """
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, LOG_LEVEL))

    # Remove any existing handlers
    root_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
