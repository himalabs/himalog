# API Reference

`get_logger`

```python
def get_logger(
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
    use_queue: bool = False,
    queue_size: int = 1000,
    use_memory_handler: bool = False,
    memory_capacity: int = 100,
    memory_flush_level: Union[int, str] = logging.ERROR,
) -> logging.Logger:
```

The main entry point for creating a logger instance. It supports console/file handlers, rotating logs, email/HTTP alerts, contextual metadata, and both synchronous and asynchronous logging strategies.

### Parameters

- `name (str, optional)` – Name of the logger. Defaults to the root logger if not provided.
- `level (int | str, optional)` – Logging level (DEBUG, INFO, WARNING, etc.). Can be int or string.
- `fmt (str, optional)` – Custom log message format string.
- `config_env (dict[str, str], optional)` – Environment-based configuration mapping (e.g., {"LOG_LEVEL": "DEBUG"}).
- `console (bool, default=True)` – Enable/disable console logging.
- `file (str, optional)` – Path to a log file for persistent storage.
- `config_path (str, optional)` – Path to YAML/JSON/TOML configuration file for external setup.

### Handler Configurations

- `rotating_file (dict, optional)` – Rotating file handler configuration. Example:
```python
{"filename": "app.log", "max_bytes": 1000000, "backup_count": 5}
```

- `timed_rotating_file (dict, optional)` – Time-based rotation config. Example:
```python
{"filename": "app.log", "when": "midnight", "backup_count": 7}
```

- `smtp_handler (dict, optional)` – Send logs via email. Example:
```python
{"mailhost": "smtp.example.com", "fromaddr": "me@example.com", "toaddrs": ["ops@example.com"], "subject": "Alert!"}
```

- `http_handler (dict, optional)` – Forward logs to HTTP endpoint. Example:
```python
{"host": "localhost:8000", "url": "/logs", "method": "POST"}
```

### Advanced Options
- `context (dict, optional)` – Contextual metadata (e.g., {"request_id": "abc123", "user": "alice"}).
- `formatter (str, optional)` – Log formatter ("json", "color", or custom).
- `filter_func (Callable, optional)` – A custom filter function to determine whether to log a record.
- `use_queue (bool, default=False)` – Enable asynchronous logging via QueueHandler/QueueListener.
- `queue_size (int, default=1000)` – Max size of async queue.
- `use_memory_handler (bool, default=False)` – Buffer logs in memory for batch writing.
- `memory_capacity (int, default=100)` – Max log records to buffer before flushing.
- `memory_flush_level (int | str, default=logging.ERROR)` – Flush buffer when this log level or higher is encountered.

### Returns
- `logging.Logger` – A fully configured logger instance.

## Examples
### Simple Console Logger
```python
logger = get_logger(name="demo", level="INFO")
logger.info("Hello, world!")
```

### With Context and JSON Formatter
```python
logger = get_logger(
    name="api",
    level="DEBUG",
    formatter="json",
    context={"request_id": "xyz789", "user": "bob"}
)
logger.warning("Something looks odd...")
```


## Handler Reference
| **Handler**             | **Config Parameters**                                                                                  | **Use Case**                                                                               |
| ----------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------ |
| **Console**             | `console=True` (default) <br> `formatter="color" \| "json" \| custom`                                  | Quick dev logs, interactive debugging, colorized output for readability.                   |
| **File**                | `file="app.log"`                                                                                       | Persistent local logging, simple audit trails.                                             |
| **Rotating File**       | `rotating_file={"filename": str, "max_bytes": int, "backup_count": int}`                               | Prevents log files from growing indefinitely by rotating when size exceeds limit.          |
| **Timed Rotating File** | `timed_rotating_file={"filename": str, "when": str, "backup_count": int}`                              | Automatically rotates logs at fixed intervals (e.g., `"midnight"`, `"H"`, `"D"`).          |
| **SMTP (Email)**        | `smtp_handler={"mailhost": str, "fromaddr": str, "toaddrs": list[str], "subject": str, "async": bool}` | Sends critical alerts to email recipients. Useful for error monitoring.                    |
| **HTTP**                | `http_handler={"host": str, "url": str, "method": "POST\|GET", "async": bool}`                         | Forwards structured logs to external services (e.g., ELK, Datadog, custom log collectors). |
| **Queue (Async)**       | `use_queue=True`, `queue_size=int`                                                                     | Offloads log handling to background thread. Ideal for high-throughput apps.                |
| **Memory (Buffered)**   | `use_memory_handler=True`, `memory_capacity=int`, `memory_flush_level=int\|str`                        | Buffers logs in memory and flushes in bulk. Reduces overhead for slow destinations.        |
