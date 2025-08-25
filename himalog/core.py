"""
Core logger logic for himalog.

This module provides the core logger class and utility functions for environment-based configuration.
"""

import logging
import os
from typing import Any, Callable, Optional, Union

_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def env_or_default(
    env: str, default: Any, cast: Callable[[str], Any] = str
) -> Any:
    """
    Get the value of an environment variable or a default, with optional casting.

    Args:
        env (str): Environment variable name.
        default (Any): Default value if env is not set or cast fails.
        cast (Callable[[str], Any], optional): Function to cast the value. Defaults to str.

    Returns:
        Any: The value from the environment or the default.
    """
    val = os.getenv(env)
    if val is not None:
        try:
            return cast(val)
        except Exception:
            return default
    return default


class HimaLog:
    """
    Core logger class for himalog.

    Handles logger instantiation, level/format configuration, and filter management.
    """

    def __init__(
        self,
        name: Optional[str] = None,
        level: Union[int, str, None] = None,
        fmt: Optional[str] = None,
        config_env: Optional[dict[str, str]] = None,
    ) -> None:
        """
        Initialize a HimaLog instance.

        Args:
            name (Optional[str]): Logger name.
            level (Union[int, str, None]): Logging level.
            fmt (Optional[str]): Log message format string.
            config_env (Optional[dict[str, str]]): Environment variable overrides.
        """
        self.logger = logging.getLogger(name)
        self._config_env = config_env or {
            "level": "HIMALOG_LEVEL",
            "format": "HIMALOG_FORMAT",
        }
        self.set_level(
            level
            or env_or_default(self._config_env["level"], logging.INFO, str)
        )
        self.set_format(
            fmt
            or env_or_default(self._config_env["format"], _DEFAULT_FORMAT, str)
        )

    def set_level(self, level: Union[int, str]) -> None:
        """
        Set the logging level.

        Args:
            level (Union[int, str]): Logging level.
        """
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(level)

    def set_format(self, fmt: str) -> None:
        """
        Set the log message format for all handlers.

        Args:
            fmt (str): Log message format string.
        """
        for handler in self.logger.handlers:
            handler.setFormatter(logging.Formatter(fmt))

    def remove_handlers(self) -> None:
        """
        Remove all handlers from the logger.
        """
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

    def add_filter(
        self, filter_func: Callable[[logging.LogRecord], bool]
    ) -> None:
        """
        Add a filter to the logger.

        Args:
            filter_func (Callable[[logging.LogRecord], bool]): Filter function.
        """
        self.logger.addFilter(filter_func)

    def remove_filter(
        self, filter_func: Callable[[logging.LogRecord], bool]
    ) -> None:
        """
        Remove a filter from the logger.

        Args:
            filter_func (Callable[[logging.LogRecord], bool]): Filter function.
        """
        self.logger.removeFilter(filter_func)

    def get_logger(self) -> logging.Logger:
        """
        Get the underlying logger instance.

        Returns:
            logging.Logger: The logger instance.
        """
        return self.logger
