import logging
from logging.handlers import HTTPHandler
from queue import Empty, Queue
from threading import Thread
from typing import Callable, Optional, Union

from ..core import _DEFAULT_FORMAT


class AsyncHTTPHandler(HTTPHandler):
    queue: "Queue[logging.LogRecord]"
    """
    An HTTPHandler that sends logs asynchronously using a background thread.
    """

    def __init__(
        self, host: str, url: str, method: str = "POST", queue_size: int = 1000
    ) -> None:
        super().__init__(host, url, method=method)
        self.queue = Queue(maxsize=queue_size)
        self._thread = Thread(target=self._worker, daemon=True)
        self._thread.start()
        self._closed = False

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self.queue.put_nowait(record)
        except Exception:
            self.handleError(record)

    def _worker(self) -> None:
        while not self._closed:
            try:
                record = self.queue.get(timeout=0.5)
                super().emit(record)
            except Empty:
                continue
            except Exception:
                pass

    def close(self) -> None:
        self._closed = True
        super().close()


def add_async_http_handler(
    logger: logging.Logger,
    host: str,
    url: str,
    method: str = "POST",
    level: Optional[Union[int, str]] = None,
    fmt: Optional[str] = None,
    filter_func: Optional[Callable[[logging.LogRecord], bool]] = None,
) -> None:
    handler: AsyncHTTPHandler = AsyncHTTPHandler(host, url, method=method)
    handler.setFormatter(logging.Formatter(fmt or _DEFAULT_FORMAT))
    if level:
        if isinstance(level, str):
            level = getattr(logging, level.upper(), logging.INFO)
        handler.setLevel(level)
    if filter_func:
        handler.addFilter(filter_func)
    logger.addHandler(handler)
