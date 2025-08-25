# Advanced Logging

The logging system provides advanced features for performance, scalability, and flexible delivery.

## Asynchronous Logging

Enable async logging for all handlers using Python’s QueueHandler/QueueListener.
This offloads log processing to a background thread, preventing I/O-bound handlers (e.g., file, HTTP, SMTP) from blocking the main application.

```python
logger = get_logger(name="myapp", use_queue=True)
logger.info("This log is handled asynchronously.")
```

✅ Best for high-throughput applications or when multiple network/disk-based handlers are configured.

## Batch/Buffered Logging

Enable log batching using MemoryHandler.
Logs are buffered in memory and only flushed when a threshold is met (record count or severity).
```python
logger = get_logger(
    name="myapp",
    use_memory_handler=True,
    memory_capacity=100,
    memory_flush_level="ERROR"
)
logger.debug("Buffered until capacity is reached.")
logger.error("This ERROR triggers an immediate flush.")
```

✅ Best for reducing overhead with slow handlers (disk, database, or HTTP).

## Async SMTP/HTTP Handlers

You can enable async delivery per handler for SMTP/HTTP independently, even if the global queue is not enabled.
This ensures that network I/O (email, HTTP POST) happens in the background.
```python
logger = get_logger(
    name="myapp",
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
)
logger.critical("This message is sent via email and HTTP asynchronously.")
```

✅ Useful for alerting systems where email/HTTP delivery should not block the app.

---

#### ⚡ Tip:
You can combine these options:

- Global async logging (use_queue=True) + Memory buffering (use_memory_handler=True) + Async SMTP/HTTP. This creates a fully non-blocking, fault-tolerant logging pipeline.