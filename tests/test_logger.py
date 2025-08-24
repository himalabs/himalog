import logging
import os
from pathlib import Path

from pytest import LogCaptureFixture

from himalog.logger import get_logger


def test_basic_console_logger(caplog: LogCaptureFixture) -> None:
    logger = get_logger("test_basic_console_logger")
    with caplog.at_level(logging.INFO):
        logger.info("Hello test!")
    assert any("Hello test!" in m for m in caplog.messages)


def test_file_handler(tmp_path: Path) -> None:
    log_file = tmp_path / "test.log"
    logger = get_logger(name="test_file_handler", file=str(log_file))
    logger.warning("File handler works!")
    with open(log_file) as f:
        content = f.read()
    assert "File handler works!" in content


def test_rotating_file_handler(tmp_path: Path) -> None:
    log_file = tmp_path / "rot.log"
    logger = get_logger(
        name="test_rotating_file_handler",
        rotating_file={
            "filename": str(log_file),
            "max_bytes": 50,
            "backup_count": 1,
        },
    )
    for i in range(10):
        logger.info(f"msg {i}")
    assert os.path.exists(log_file)


def test_timed_rotating_file_handler(tmp_path: Path) -> None:
    log_file = tmp_path / "timed.log"
    logger = get_logger(
        name="test_timed_rotating_file_handler",
        timed_rotating_file={
            "filename": str(log_file),
            "when": "S",
            "interval": 1,
            "backup_count": 1,
        },
    )
    logger.info("timed rotation test")
    assert os.path.exists(log_file)


def test_json_formatter(caplog: LogCaptureFixture) -> None:
    logger = get_logger("test_json_formatter", formatter="json")
    with caplog.at_level(logging.INFO):
        logger.info("json test")
    assert any("json test" in m for m in caplog.messages)


def test_color_formatter(caplog: LogCaptureFixture) -> None:
    logger = get_logger("test_color_formatter", formatter="color")
    with caplog.at_level(logging.INFO):
        logger.info("color test")
    assert any("color test" in m for m in caplog.messages)


def test_contextual_logging(caplog: LogCaptureFixture) -> None:
    logger = get_logger("test_contextual_logging", context={"user": "alice"})
    with caplog.at_level(logging.INFO):
        logger.info("context test")
    assert any("context test" in m for m in caplog.messages)
