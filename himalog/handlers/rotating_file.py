import logging
import logging.handlers
from typing import Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


def add_rotating_file_handler(
    logger: logging.Logger,
    filename: str,
    max_bytes: int = 1048576,
    backup_count: int = 3,
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    rfh = logging.handlers.RotatingFileHandler(
        filename, maxBytes=max_bytes, backupCount=backup_count
    )
    rfh.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        rfh.setLevel(level)
    if filter_func:
        rfh.addFilter(filter_func)
    logger.addHandler(rfh)
