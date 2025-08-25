"""
Formatters for himalog loggers.

Includes JSON and colorized formatters for advanced log output.
"""

import json
import logging


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs logs in JSON format.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as a JSON string.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: JSON-formatted log string.
        """
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "name": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)


class ColorFormatter(logging.Formatter):
    """
    Formatter that outputs colorized log messages for the console.
    """

    COLORS = {
        "DEBUG": "\033[94m",
        "INFO": "\033[92m",
        "WARNING": "\033[93m",
        "ERROR": "\033[91m",
        "CRITICAL": "\033[95m",
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record as a colorized string.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            str: Colorized log string.
        """
        color = self.COLORS.get(record.levelname, self.RESET)
        time = self.formatTime(record, self.datefmt)
        name = record.name.ljust(15)
        level = record.levelname.ljust(8)
        msg = record.getMessage()
        # Add context fields if present
        context = ""
        for attr in sorted(vars(record)):
            if attr not in (
                "name",
                "levelname",
                "msg",
                "args",
                "created",
                "msecs",
                "relativeCreated",
                "levelno",
                "pathname",
                "filename",
                "module",
                "exc_info",
                "exc_text",
                "stack_info",
                "lineno",
                "funcName",
                "thread",
                "threadName",
                "processName",
                "process",
                "message",
                "asctime",
            ):
                value = getattr(record, attr)
                if not attr.startswith("_") and not callable(value):
                    context += f" {attr}={value}"
        formatted = (
            f"{color}{time} [{level}] {name}: {msg}{context}{self.RESET}"
        )
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        return formatted
