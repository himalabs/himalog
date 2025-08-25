import time

import pytest

from himalog.logger import get_logger


def test_async_http_handler(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that the async HTTP handler queues logs and calls emit in a background thread.
    """
    emitted = []

    import logging

    def fake_emit(self: object, record: logging.LogRecord) -> None:
        emitted.append(record.getMessage())

    monkeypatch.setattr("logging.handlers.HTTPHandler.emit", fake_emit)
    logger = get_logger(
        name="test_async_http_handler",
        http_handler={
            "host": "localhost",
            "url": "/log",
            "method": "POST",
            "async": True,
        },
    )
    logger.error("async http test")
    # Wait for background thread to process
    for _ in range(10):
        if emitted:
            break
        time.sleep(0.1)
    assert any("async http test" in msg for msg in emitted)


def test_async_smtp_handler(monkeypatch: pytest.MonkeyPatch) -> None:
    """
    Test that the async SMTP handler queues logs and calls emit in a background thread.
    """
    emitted = []

    import logging

    def fake_emit(self: object, record: logging.LogRecord) -> None:
        emitted.append(record.getMessage())

    monkeypatch.setattr("logging.handlers.SMTPHandler.emit", fake_emit)
    logger = get_logger(
        name="test_async_smtp_handler",
        smtp_handler={
            "mailhost": "localhost",
            "fromaddr": "from@example.com",
            "toaddrs": ["to@example.com"],
            "subject": "Test",
            "async": True,
        },
    )
    logger.critical("async smtp test")
    # Wait for background thread to process
    for _ in range(10):
        if emitted:
            break
        time.sleep(0.1)
    assert any("async smtp test" in msg for msg in emitted)
