# Configuration

Himalog supports flexible configuration methods to adapt to different environments and deployment strategies.
You can configure logging via:

1. Code-based setup (using get_logger)
2. Configuration files (YAML, JSON, TOML)
3. Environment variables (for overrides)

## Example YAML config

```yaml
name: myapp
level: INFO
file: app.log
rotating_file:
  filename: app_rot.log
  max_bytes: 1000000
  backup_count: 5
timed_rotating_file:
  filename: app_time.log
  when: midnight
  backup_count: 7
smtp_handler:
  mailhost: smtp.example.com
  fromaddr: from@example.com
  toaddrs:
    - to@example.com
  subject: Log Alert
  async: true
http_handler:
  host: localhost:8000
  url: /log
  method: POST
  async: true
formatter: color
context:
  request_id: abc123
  user: alice
use_queue: true
use_memory_handler: true
```
## Usage
```python
logger = get_logger(config_path="logging.yaml")
logger.info("Logger configured from YAML file")

```



## Environment Variables

Any configuration option can be overridden with environment variables.
This is especially useful for containerized or cloud deployments, where config files may not be practical.

Example:

```badh
export LOG_LEVEL=DEBUG
export LOG_FILE=/var/log/myapp.log
```

Then in code:
```python
logger = get_logger(name="myapp", config_env=os.environ)
```

### Config Precedence
When multiple sources are used, Himalog applies settings in this order (lowest → highest priority):
1. Defaults (built-in)
2. Config file (YAML/JSON/TOML via config_path)
3. Environment variables (config_env)
4. Code arguments (explicit get_logger parameters)

This makes it easy to provide sensible defaults, while still allowing environment-specific overrides.