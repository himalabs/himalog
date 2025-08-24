import logging
import logging.handlers
from typing import Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


def add_timed_rotating_file_handler(
    logger: logging.Logger,
    filename: str,
    when: str = "midnight",
    interval: int = 1,
    backup_count: int = 7,
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    t_handler = logging.handlers.TimedRotatingFileHandler(
        filename, when=when, interval=interval, backupCount=backup_count
    )
    t_handler.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        t_handler.setLevel(level)
    if filter_func:
        t_handler.addFilter(filter_func)
    logger.addHandler(t_handler)
