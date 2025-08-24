import logging
from logging.handlers import HTTPHandler
from typing import Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


def add_http_handler(
    logger: logging.Logger,
    host: str,
    url: str,
    method: str = "POST",
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    handler = HTTPHandler(host, url, method=method)
    handler.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        handler.setLevel(level)
    if filter_func:
        handler.addFilter(filter_func)
    logger.addHandler(handler)
