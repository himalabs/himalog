"""
Configuration loader for himalog.
Supports YAML, JSON, and TOML config files.
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


def get_config_from_env(
    env_var: str = "HIMALOG_CONFIG",
) -> Any:
    path = os.getenv(env_var)
    if path and os.path.isfile(path):
        return load_config(path)
    return None
