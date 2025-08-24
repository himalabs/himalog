import logging
from typing import Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


def add_file_handler(
    logger: logging.Logger,
    filename: str,
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    fh = logging.FileHandler(filename)
    fh.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        fh.setLevel(level)
    if filter_func:
        fh.addFilter(filter_func)
    logger.addHandler(fh)
