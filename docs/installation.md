# Installation

Install Himalog from PyPI with pip (recommended for most users):

```powershell
# PowerShell / Windows
python -m pip install himalog
```

```bash
# macOS / Linux
python3 -m pip install himalog
```

Specify a version to pin a release:

```powershell
python -m pip install himalog==0.2.0
```

## Install from source (editable / development)

If you want to hack on the library or run the test suite locally, clone the repository and install in editable mode.

```powershell
# clone the repo
git clone https://github.com/himalabs/himalog.git
cd himalog

# Windows (PowerShell) editable install using pip
python -m pip install -e .

# or using Poetry (recommended for project development)
poetry install
poetry shell
```

On macOS / Linux use `python3` instead of `python` where appropriate.

## Using Poetry

Himalog uses Poetry for project metadata in this repository. To create a dev environment and install dependencies:

```powershell
# install dependencies and dev-deps
poetry install
# open a shell with the virtual environment
poetry shell
```

Run tests from the project root inside the poetry shell:

```powershell
pytest -q
```

## Pipenv

For Pipenv users:

```bash
pipenv install himalog
# or to install the local checkout for development
pipenv install -e .
```

## Installing with requirements files

If you manage dependencies with a `requirements.txt`, add `himalog` to it and install normally:

```bash
pip install -r requirements.txt
```

## Installing directly from GitHub

To install the latest code directly from the main repository (not recommended for production):

```bash
pip install git+https://github.com/himalabs/himalog.git@feat/logger
```

Replace the branch or tag as needed.

## Optional / extra dependencies

If the project exposes optional features that require extra packages (for example SMTP helpers, HTTP client libraries, or JSON helpers), install the extras as documented in the package metadata. Example:

```bash
pip install himalog[http]
```

(see the package README or `pyproject.toml` for available extras)

## Verifying the installation

Quick smoke test — start a Python REPL and import the library:

```powershell
python -c "import himalog; print(himalog.__version__)"
```

A quick usage check:

```python
from himalog.logger import get_logger
logger = get_logger(name="demo", level="INFO")
logger.info("Himalog installation OK")
```

Save the snippet above to a file and run it to ensure basic runtime behavior.

## Troubleshooting & tips

- Use virtual environments (venv, Poetry, Pipenv) to avoid permission and dependency conflicts.
- On Windows ensure `python` points to the correct interpreter (use the full path or `py -3`).
- If a handler needs write access to a directory (file/rotating handlers), ensure the directory exists and the process has write permissions.
- When installing from source, run the test suite (`pytest`) to validate the local environment.
- If you rely on SMTP or external HTTP endpoints during tests, prefer to mock those in CI to avoid flakiness.
