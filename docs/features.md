---
title: Features — Himalog
---

# Features — Himalog

Himalog is a lightweight, production-oriented Python logging toolkit built on top of the standard
`logging` module. It focuses on three practical goals:

- Make logging easy to configure (code, env, or config files).
- Make logging safe and non-blocking for production workloads (async/queue/batching).
- Make logs structured and contextual for observability pipelines.

This document describes the main features, recommended usage patterns, and short examples.

## 1. Modular handler system

Himalog exposes helpers to create and wire common handlers so you can pick the right
destination(s) for each deployment:

- **ConsoleHandler** — standard output with optional colorized formatting for local development.
- **FileHandler** — simple file-based logging.
- **RotatingFileHandler** — size-based rotation with backup retention.
- **TimedRotatingFileHandler** — time-based rotation (daily/hourly, etc.).
- **SMTPHandler** — send high-severity events by email.
- **HTTPHandler** — post log records to an HTTP endpoint (JSON payloads).

Handlers are modular: mix and match multiple handlers for the same logger. Each handler can use
either a structured JSON formatter or a human-friendly color formatter.

## 2. Asynchronous logging (recommended for I/O-bound handlers)

To avoid blocking application threads on slow I/O (disk, network, SMTP), Himalog supports two
levels of asynchrony:

1. Per-handler async wrappers (e.g. `AsyncHTTPHandler`, `AsyncSMTPHandler`) — these enqueue records
   and send them from a background thread.
2. Global `QueueHandler` + `QueueListener` — offload all handler-emission work to a background
   consumer thread. This is the recommended approach for high-throughput applications.

Benefits:

- Minimal latency impact on the main thread.
- Better resilience against transient network or SMTP failures (you can buffer/retry).

Example: enable a queue-based logger

```python
from himalog.logger import get_logger

logger = get_logger(
    name="myapp",
    level="INFO",
    use_queue=True,          # enable QueueHandler + QueueListener
    queue_size=2048,         # max queued records
)

logger.info("startup complete", extra={"service": "myapp"})
```

## 3. Batch / buffered logging (MemoryHandler)

For very slow or high-latency backends, wrap those handlers with a `MemoryHandler` to buffer
records in memory and flush them in bulk either by size or by level. `MemoryHandler` reduces
syscalls and network calls by grouping records.

Example: buffer writes for a remote file or HTTP handler

```python
logger = get_logger(
    name="myapp",
    use_memory_handler=True,
    memory_capacity=500,           # keep up to 500 records in memory
    memory_flush_level="ERROR",  # force flush on ERROR or higher
)
```

You can combine `MemoryHandler` and `use_queue` for both batching and non-blocking delivery.

## 4. Contextual logging

Himalog supports injecting contextual metadata into every log record via a lightweight filter
(`ContextFilter`). Use it to attach request ids, user ids, correlation ids, or any per-request
state so downstream systems can reconstruct traces.

Example: adding a request_id to every record

```python
logger = get_logger(name="myapp")
# The public API exposes a way to attach context via filters; in frameworks, prefer middleware
# to set context per request.
logger.info("handling request", extra={"request_id": "abc123"})
```

When integrated into web frameworks (FastAPI/Django/Flask), add the context in middleware so each
request has its own metadata.

## 5. Formatters: JSON and colorized output

- **JSONFormatter** — outputs structured JSON records (timestamp, level, message, and extra fields).
  Use this for log aggregation systems like ELK, Splunk, or cloud logging services.
- **ColorFormatter** — human-friendly ANSI colored output for console use.

Example: choose JSON output for production

```python
logger = get_logger(name="myapp", formatter="json")
```

## 6. Flexible configuration

You can configure Himalog via:

- Code (the `get_logger()` API) — best for programmatic control and tests.
- Environment variables — quick switches for log level or enabling queueing.
- YAML/JSON/TOML config files — suitable for operations teams and deployment automation.

The config loaders in `himalog.config` accept common file formats. Prefer declarative configs in
production so operations can tune logging without a code change.

## 7. Robustness and graceful degradation

Himalog uses defensive handler setup. If a handler fails to initialize (for example, due to a
missing directory or network problem), the library can fall back to console logging so critical
messages remain visible.

Additionally, background async handlers handle transient errors and avoid crashing the main
application thread.

## 8. Type-annotated and mypy-friendly

All public APIs and handlers include type annotations for better IDE support and static checks
with `mypy`. Tests are also type-annotated to keep the project consistent.

## Recommended patterns and examples

- Development

  - Use `ConsoleHandler` with `ColorFormatter` and `DEBUG` level.

- Production (high throughput)

  - Use `JSONFormatter` and enable `use_queue=True`.
  - Wrap slow handlers with `MemoryHandler` and tune `memory_capacity`.

- Critical alerts

  - Keep an `SMTPHandler` (or async SMTP wrapper) for critical errors and configure rate
    limiting at the application or SMTP gateway level.

## Implementation notes

- Per-handler async wrappers use a single background thread and an internal queue to avoid
  blocking the emitter thread.
- Global queue mode leverages `logging.handlers.QueueHandler` and `QueueListener` from the
  standard library and is the recommended, scalable approach.

## Use cases

- Local development: colorized console logs.
- Containerized production: JSON logs written to stdout and collected by the container runtime.
- High-throughput services: queue-enabled loggers with batched flushes.
