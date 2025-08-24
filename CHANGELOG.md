# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v0.1.2 - (2025-08-24)

### Added
- SMTP handler support: send logs via email using SMTPHandler.
- HTTP handler support: send logs to remote HTTP endpoints using HTTPHandler.
- Contextual logging support: inject context (e.g., request IDs, user info) into all log records via config or code.
- Robust error handling: handler setup is now wrapped in a safe function that logs errors if a handler fails to initialize, preventing logger crashes.
- Beautiful, structured, and colorful logs: ColorFormatter now outputs aligned fields and context fields for enhanced readability (emoji removed for professional output).

## v0.1.1 - (2025-07-28)

### Added
- `CHANGELOG.md` for release notes and keeping changes logged.
- `CODE_OF_CONDUCT.md` to enforce strong community rules for safer environment.
- `CONTRIBUTING.md` guide for making contribution to the project and community.


## v0.1.0 - (2025-07-27)

### Added

- `poetry.lock` file to lock dependency versions.
- `pyproject.toml` file for project configuration.
- Initial package structure with `himalog` and `tests` directories.
- Added `hello_world` function in `himalog/hello_world.py` that returns a simple "Hello, world!" string.
- Added test for `hello_world` in `tests/test_hello_world.py`.
- Github workflows `publish-package.yml` and `run-test.yml`.