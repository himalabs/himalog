# himalog
🏔️ Himalog – A Sleek, Self-Hosted Live Log Viewer for Developers

## Features

- Simple `hello_world` function for demonstration and testing purposes.
- Automated tests using pytest.
- CI workflow for linting, formatting (Black), and type checking (mypy, flake8) on every push and pull request to `main`.

## Getting Started

Install dependencies:

```bash
uv sync --python 3.10 --frozen
```

Run formatting, lint, and type checks:

```bash
make format
make lint
make typecheck
```

Run tests:

```bash
pytest
```

## Contributing

Please ensure your code passes formatting, lint, and type checks before submitting a pull request. All checks run automatically in CI.
