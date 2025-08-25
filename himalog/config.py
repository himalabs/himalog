"""
Configuration loader for himalog.

Supports YAML, JSON, and TOML config files for flexible logger configuration.
"""

import json
import os
from typing import Any

try:
    import yaml as _yaml
except ImportError:
    _yaml = None  # type: ignore
try:
    import toml as _toml
except ImportError:
    _toml = None  # type: ignore


def load_config(config_path: str) -> Any:
    """
    Load a configuration file (YAML, JSON, or TOML).

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        Any: Parsed configuration data.

    Raises:
        ImportError: If required parser is not installed.
        ValueError: If the file extension is unsupported.
    """
    ext = os.path.splitext(config_path)[1].lower()
    with open(config_path, "r", encoding="utf-8") as f:
        if ext in [".yaml", ".yml"]:
            if not _yaml or not getattr(_yaml, "safe_load", None):
                raise ImportError("pyyaml is required for YAML config support")
            return _yaml.safe_load(f)
        elif ext == ".json":
            return json.load(f)
        elif ext == ".toml":
            if not _toml or not getattr(_toml, "load", None):
                raise ImportError("toml is required for TOML config support")
            return _toml.load(f)
        else:
            raise ValueError(f"Unsupported config file extension: {ext}")


def get_config_from_env(env_var: str = "HIMALOG_CONFIG") -> Any:
    """
    Load configuration from an environment variable if set.

    Args:
        env_var (str, optional): Name of the environment variable. Defaults to "HIMALOG_CONFIG".

    Returns:
        Any: Parsed configuration data or None if not found.
    """
    path = os.getenv(env_var)
    if path and os.path.isfile(path):
        return load_config(path)
    return None
