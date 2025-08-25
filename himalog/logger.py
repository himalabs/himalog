"""
himalog.logger
Public API for the himalog logging system.
"""

import logging
from typing import Any, Callable, Optional, Union

from .config import load_config
from .core import _DEFAULT_FORMAT, HimaLog
from .formatters import ColorFormatter, JsonFormatter
from .handlers.async_http import add_async_http_handler
from .handlers.async_smtp import add_async_smtp_handler
from .handlers.console import add_console_handler
from .handlers.file import add_file_handler
from .handlers.http import add_http_handler
from .handlers.rotating_file import add_rotating_file_handler
from .handlers.smtp import add_smtp_handler
from .handlers.timed_rotating_file import add_timed_rotating_file_handler


def get_logger(
    use_queue: bool = False,
    queue_size: int = 1000,
    use_memory_handler: bool = False,
    memory_capacity: int = 100,
    memory_flush_level: Union[int, str] = logging.ERROR,
    name: Optional[str] = None,
    level: Union[int, str, None] = None,
    fmt: Optional[str] = None,
    config_env: Optional[dict[str, str]] = None,
    console: bool = True,
    file: Optional[str] = None,
    config_path: Optional[str] = None,
    rotating_file: Optional[dict[str, Any]] = None,
    timed_rotating_file: Optional[dict[str, Any]] = None,
    context: Optional[dict[str, Any]] = None,
    formatter: Optional[str] = None,
    smtp_handler: Optional[dict[str, Any]] = None,
    http_handler: Optional[dict[str, Any]] = None,
    filter_func: Optional[Callable[..., bool]] = None,
) -> logging.Logger:
    """
    Get a configured logger with advanced features.

    Args:
        name (Optional[str]): Logger name. Defaults to None (root logger).
        level (Union[int, str, None]): Logging level. Defaults to None.
        fmt (Optional[str]): Log message format string. Defaults to None.
        config_env (Optional[dict[str, str]]): Environment variable overrides. Defaults to None.
        console (bool): Add console handler. Defaults to True.
        file (Optional[str]): File path for file handler. Defaults to None.
        config_path (Optional[str]): Path to config file (YAML/JSON/TOML). Defaults to None.
        rotating_file (Optional[dict[str, Any]]): Rotating file handler config. Defaults to None.
        timed_rotating_file (Optional[dict[str, Any]]): Timed rotating file handler config. Defaults to None.
        context (Optional[dict[str, Any]]): Contextual fields to add to log records. Defaults to None.
        formatter (Optional[str]): Formatter type ('color', 'json', or None). Defaults to None.
        smtp_handler (Optional[dict[str, Any]]): SMTP handler config. Defaults to None.
        http_handler (Optional[dict[str, Any]]): HTTP handler config. Defaults to None.
        filter_func (Optional[Callable[..., bool]]): Custom filter function. Defaults to None.

    Args:
        use_queue (bool): If True, use QueueHandler/QueueListener for async logging.
        queue_size (int): Max size of the log queue.
        use_memory_handler (bool): If True, wrap handlers in a MemoryHandler for batching.
        memory_capacity (int): Buffer size for MemoryHandler.
        memory_flush_level (Union[int, str]): Level at which MemoryHandler flushes.

    Returns:
        logging.Logger: Configured logger instance.
    """
    config = None
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
        """
        Logging filter to inject contextual fields into log records.

        Args:
            context (Optional[dict[str, Any]]): Contextual fields to add.
        """

        def __init__(self, context: Optional[dict[str, Any]] = None) -> None:
            super().__init__()
            self.context: dict[str, Any] = context or {}

        def filter(self, record: logging.LogRecord) -> bool:
            """
            Add context fields to the log record.

            Args:
                record (logging.LogRecord): The log record.

            Returns:
                bool: Always True.
            """
            for k, v in self.context.items():
                setattr(record, k, v)
            return True

    context_filter: Optional[ContextFilter] = None
    if context:
        context_filter = ContextFilter(context)

    def safe_add_handler(
        add_func: Callable[..., None], *args: Any, **kwargs: Any
    ) -> None:
        """
        Safely add a logging handler, catching and logging errors.

        Args:
            add_func (Callable[..., None]): Handler addition function.
            *args: Positional arguments for handler.
            **kwargs: Keyword arguments for handler.
        """
        try:
            add_func(*args, **kwargs)
        except Exception as e:
            logging.getLogger("himalog").error(f"Failed to add handler: {e}")

    import queue
    from logging.handlers import MemoryHandler, QueueHandler, QueueListener

    hima_log = HimaLog(name, level, fmt, config_env)
    logger = hima_log.get_logger()
    if context_filter:
        logger.addFilter(context_filter)

    # Collect handlers to attach (for queue/memory support)
    from typing import List

    handlers: List[logging.Handler] = []
    if console:
        ch_logger = logging.getLogger(f"{name or 'root'}-console")
        safe_add_handler(
            add_console_handler,
            ch_logger,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
        handlers.extend(ch_logger.handlers)
        ch_logger.handlers.clear()
    if file:
        fh_logger = logging.getLogger(f"{name or 'root'}-file")
        safe_add_handler(
            add_file_handler,
            fh_logger,
            file,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
        handlers.extend(fh_logger.handlers)
        fh_logger.handlers.clear()
    if rotating_file:
        rfh_logger = logging.getLogger(f"{name or 'root'}-rotfile")
        safe_add_handler(
            add_rotating_file_handler,
            rfh_logger,
            **rotating_file,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
        handlers.extend(rfh_logger.handlers)
        rfh_logger.handlers.clear()
    if timed_rotating_file:
        trfh_logger = logging.getLogger(f"{name or 'root'}-timedrotfile")
        safe_add_handler(
            add_timed_rotating_file_handler,
            trfh_logger,
            **timed_rotating_file,
            level=level,
            fmt=fmt,
            filter_func=filter_func,
        )
        handlers.extend(trfh_logger.handlers)
        trfh_logger.handlers.clear()
    if smtp_handler:
        smtp_logger = logging.getLogger(f"{name or 'root'}-smtp")
        if smtp_handler.get("async"):
            safe_add_handler(
                add_async_smtp_handler,
                smtp_logger,
                **{k: v for k, v in smtp_handler.items() if k != "async"},
            )
        else:
            safe_add_handler(add_smtp_handler, smtp_logger, **smtp_handler)
        handlers.extend(smtp_logger.handlers)
        smtp_logger.handlers.clear()
    if http_handler:
        http_logger = logging.getLogger(f"{name or 'root'}-http")
        if http_handler.get("async"):
            safe_add_handler(
                add_async_http_handler,
                http_logger,
                **{k: v for k, v in http_handler.items() if k != "async"},
            )
        else:
            safe_add_handler(add_http_handler, http_logger, **http_handler)
        handlers.extend(http_logger.handlers)
        http_logger.handlers.clear()

    # Optionally wrap handlers in MemoryHandler for batching
    if use_memory_handler:
        wrapped: List[logging.Handler] = []
        flush_level = memory_flush_level
        if isinstance(flush_level, str):
            flush_level = getattr(logging, flush_level.upper(), logging.ERROR)
        for h in handlers:
            memh = MemoryHandler(
                memory_capacity, flushLevel=flush_level, target=h
            )
            wrapped.append(memh)
        handlers = wrapped

    # Optionally use QueueHandler/QueueListener for async logging
    if use_queue:
        log_queue: "queue.Queue[logging.LogRecord]" = queue.Queue(
            maxsize=queue_size
        )
        qh = QueueHandler(log_queue)
        logger.addHandler(qh)
        listener = QueueListener(
            log_queue, *handlers, respect_handler_level=True
        )
        listener.start()
    else:
        for h in handlers:
            logger.addHandler(h)

    # Apply formatter to all handlers if specified
    if formatter_obj:
        for handler in logger.handlers:
            handler.setFormatter(formatter_obj)
    assert isinstance(logger, logging.Logger)
    return logger
