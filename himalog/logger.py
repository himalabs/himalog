"""
himalog.logger
Public API for the himalog logging system.
"""

import logging
from typing import Any, Callable, Optional, Union

from .config import load_config
from .core import _DEFAULT_FORMAT, HimaLog
from .formatters import ColorFormatter, JsonFormatter
from .handlers.console import add_console_handler
from .handlers.file import add_file_handler
from .handlers.http import add_http_handler
from .handlers.rotating_file import add_rotating_file_handler
from .handlers.smtp import add_smtp_handler
from .handlers.timed_rotating_file import add_timed_rotating_file_handler


def get_logger(
    name: Optional[str] = None,
    level: Union[int, str, None] = None,
    fmt: Optional[str] = None,
    config_env: Optional[dict[str, str]] = None,
    console: bool = True,
    file: Optional[str] = None,
    config_path: Optional[str] = None,
    timed_rotating_file: Optional[dict[str, Any]] = None,
    formatter: Optional[str] = None,
    smtp_handler: Optional[dict[str, Any]] = None,
    http_handler: Optional[dict[str, Any]] = None,
    filter_func: Optional[Callable[..., bool]] = None,
) -> logging.Logger:
    """Get a configured logger. See documentation for all options."""
    config = None
    rotating_file = None
    if config_path:
        config = load_config(config_path)
    if config:
        name = config.get("name", name)
        level = config.get("level", level)
        fmt = config.get("fmt", fmt)
        config_env = config.get("config_env", config_env)
        console = config.get("console", console)
        file = config.get("file", file)
        rotating_file = config.get("rotating_file", rotating_file)
        timed_rotating_file = config.get(
            "timed_rotating_file", timed_rotating_file
        )
        formatter = config.get("formatter", formatter)
    # Formatter selection
    formatter_obj: Optional[Union[ColorFormatter, JsonFormatter]] = None
    if formatter == "json":
        formatter_obj = JsonFormatter()
    elif formatter == "color":
        formatter_obj = ColorFormatter(fmt or _DEFAULT_FORMAT)

    # Contextual logging support
    class ContextFilter(logging.Filter):
        def __init__(self, context: Optional[dict[str, Any]] = None) -> None:
            super().__init__()
            self.context: dict[str, Any] = context or {}

        def filter(self, record: logging.LogRecord) -> bool:
            for k, v in self.context.items():
                setattr(record, k, v)
            return True

    context: Optional[dict[str, Any]] = (
        config.get("context") if config else None
    )
    context_filter: Optional[ContextFilter] = None
    if context:
        context_filter = ContextFilter(context)

    def safe_add_handler(
        add_func: Callable[..., None], *args: Any, **kwargs: Any
    ) -> None:
        try:
            add_func(*args, **kwargs)
        except Exception as e:
            logging.getLogger("himalog").error(f"Failed to add handler: {e}")

    hima_log = HimaLog(name, level, fmt, config_env)
    logger = hima_log.get_logger()
    if context_filter:
        logger.addFilter(context_filter)
    if console:
        safe_add_handler(
            add_console_handler,
            logger,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
    if file:
        safe_add_handler(
            add_file_handler,
            logger,
            file,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
    if rotating_file:
        safe_add_handler(
            add_rotating_file_handler,
            logger,
            **rotating_file,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
    if timed_rotating_file:
        safe_add_handler(
            add_timed_rotating_file_handler,
            logger,
            **timed_rotating_file,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
    if smtp_handler:
        safe_add_handler(add_smtp_handler, logger, **smtp_handler)
    if http_handler:
        safe_add_handler(add_http_handler, logger, **http_handler)
    # Apply formatter to all handlers if specified
    if formatter_obj:
        for handler in logger.handlers:
            handler.setFormatter(formatter_obj)
    assert isinstance(logger, logging.Logger)
    return logger
