# Usage

## Basic Example

For a quick start, you can obtain a logger with minimal configuration:
```python
from himalog.logger import get_logger

logger = get_logger(name="myapp")
logger.info("Hello from himalog!")
```

- Creates a logger named myapp.
- Defaults to console output with standard formatting.
- Suitable for development and quick prototyping.

## Advanced Example
For production environments, you can configure multiple handlers, advanced formatters, and asynchronous logging:

```python
from himalog.logger import get_logger

logger = get_logger(
    name="myapp",
    level="DEBUG",
    file="app.log",
    rotating_file={"filename": "app_rot.log", "max_bytes": 1000000, "backup_count": 5},
    timed_rotating_file={"filename": "app_time.log", "when": "midnight", "backup_count": 7},
    smtp_handler={
        "mailhost": "smtp.example.com",
        "fromaddr": "from@example.com",
        "toaddrs": ["to@example.com"],
        "subject": "Log Alert",
        "async": True
    },
    http_handler={
        "host": "localhost:8000",
        "url": "/log",
        "method": "POST",
        "async": True
    },
    formatter="color",
    context={"request_id": "abc123", "user": "alice"},
    use_queue=True,
    use_memory_handler=True,
)

logger.debug("This will go to all configured handlers asynchronously and/or in batches.")
```

## Explanation of Options
- `level="DEBUG"` → Set minimum log level.
- `file="app.lo`g" → Standard file logging.
- `rotating_file={...}` → Rotates log file when it reaches max_bytes, keeping backup_count files.
- `timed_rotating_file={...}` → Rotates logs at a specified interval (e.g., midnight).
- `smtp_handler={...}` → Sends logs via email for critical alerts, optionally asynchronously.
- `http_handler={...}` → Posts logs to an HTTP endpoint in JSON format, optionally asynchronously.
- `formatter="col`or" → Use colorized console output; "json" is also supported.
- `context={...} → Enrich`es logs with metadata like request_id and user.
- `use_queue=True` → Enables asynchronous logging via QueueHandler/QueueListener.
- `use_memory_handler=True` → Buffers logs in memory and flushes in batches.

## ✅ This setup ensures:
- Scalable logging (asynchronous + buffered).
- Multiple destinations (console, files, email, HTTP).
- Context-rich structured logs (trace requests, users, etc.).
- Readable dev output (colorized) and machine-friendly prod output (JSON).