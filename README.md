
# himalog

Himalog – Flexible, Modular Logging for Python Applications


## Features

- Extensible logging system for Python
- Modular handlers: console, file, rotating, timed rotating, SMTP, HTTP
- Configurable via code, environment variables, or YAML/JSON/TOML
- Contextual logging (add request/user info, etc.)
- JSON and colorized formatters (aligned fields, context)
- Robust error handling for handler setup

## Install

```bash
pip install himalog
```

## Usage

```python
from himalog.logger import get_logger

# Basic usage
logger = get_logger("myapp")
logger.info("Hello from himalog!")

# Advanced usage
logger = get_logger(
	name="myapp",
	level="DEBUG",
	file="app.log",
	rotating_file={"filename": "app_rot.log", "max_bytes": 1000000, "backup_count": 5},
	timed_rotating_file={"filename": "app_time.log", "when": "midnight", "backup_count": 7},
	smtp_handler={"mailhost": "smtp.example.com", "fromaddr": "from@example.com", "toaddrs": ["to@example.com"], "subject": "Log Alert"},
	http_handler={"host": "localhost:8000", "url": "/log", "method": "POST"},
	formatter="color",  # or "json" for structured logs
	context={"request_id": "abc123", "user": "alice"}
)
logger.debug("This will go to all configured handlers.")
```

`get_logger` supports the following arguments:

- `name`: Logger name (str)
- `level`: Log level (str or int, e.g. "INFO", "DEBUG")
- `fmt`: Log format string (optional)
- `config_env`: Dict of environment variable names for config (optional)
- `console`: Add console handler (bool, default True)
- `file`: Add file handler (str, filename)
- `rotating_file`: Dict for rotating file handler (keys: filename, max_bytes, backup_count)
- `timed_rotating_file`: Dict for timed rotating file handler (keys: filename, when, backup_count, ...)
- `smtp_handler`: Dict for SMTP handler (keys: mailhost, fromaddr, toaddrs, subject, ...)
- `http_handler`: Dict for HTTP handler (keys: host, url, method, ...)
- `formatter`: "color" for color logs, "json" for structured logs, or None
- `context`: Dict of extra fields to inject into all log records (e.g. request_id, user)
- `config_path`: Path to YAML/JSON/TOML config file (optional)
- `filter_func`: Custom filter function (optional)

---

## Project Structure

- `himalog/core.py`: Core logger logic
- `himalog/handlers/`: Console, file, and rotating file handler modules
- `himalog/logger.py`: Public API for logger creation and configuration

## Contributing

Please ensure your code passes formatting, lint, and type checks before submitting a pull request. All checks run automatically in CI.
