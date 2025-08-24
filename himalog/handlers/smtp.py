import logging
from logging.handlers import SMTPHandler
from typing import Optional, Union, Callable
from ..core import _DEFAULT_FORMAT


def add_smtp_handler(
    logger: logging.Logger,
    mailhost: str,
    fromaddr: str,
    toaddrs: list,
    subject: str,
    credentials: Optional[tuple] = None,
    secure: Optional[tuple] = None,
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable] = None,
):
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
