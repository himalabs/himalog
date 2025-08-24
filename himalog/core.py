"""
Core logger logic for himalog.
"""

import logging
import os
from typing import Any, Callable, Optional, Union

_DEFAULT_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


def env_or_default(
    env: str, default: Any, cast: Callable[[str], Any] = str
) -> Any:
    val = os.getenv(env)
    if val is not None:
        try:
            return cast(val)
        except Exception:
            return default
    return default


class HimaLog:
    def __init__(
        self,
        name: Optional[str] = None,
        level: Union[int, str, None] = None,
        fmt: Optional[str] = None,
        config_env: Optional[dict[str, str]] = None,
    ) -> None:
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
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        self.logger.setLevel(level)

    def set_format(self, fmt: str) -> None:
        for handler in self.logger.handlers:
            handler.setFormatter(logging.Formatter(fmt))

    def remove_handlers(self) -> None:
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)

    def add_filter(
        self, filter_func: Callable[[logging.LogRecord], bool]
    ) -> None:
        self.logger.addFilter(filter_func)

    def remove_filter(
        self, filter_func: Callable[[logging.LogRecord], bool]
    ) -> None:
        self.logger.removeFilter(filter_func)

    def get_logger(self) -> logging.Logger:
        return self.logger
