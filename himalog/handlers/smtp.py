import logging
from logging.handlers import SMTPHandler
from typing import Any, Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


def add_smtp_handler(
    logger: logging.Logger,
    mailhost: str,
    fromaddr: str,
    toaddrs: list[str],
    subject: str,
    credentials: Optional[tuple[str, str]] = None,
    secure: Optional[tuple[Any, ...]] = None,
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    handler = SMTPHandler(
        mailhost,
        fromaddr,
        toaddrs,
        subject,
        credentials=credentials,
        secure=secure,
    )
    handler.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        handler.setLevel(level)
    if filter_func:
        handler.addFilter(filter_func)
    logger.addHandler(handler)
