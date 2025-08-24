import logging
from typing import Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


def add_console_handler(
    logger: logging.Logger,
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        ch.setLevel(level)
    if filter_func:
        ch.addFilter(filter_func)
    logger.addHandler(ch)
