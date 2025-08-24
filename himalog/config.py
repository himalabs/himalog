"""
Configuration loader for himalog.
Supports YAML, JSON, and TOML config files.
"""

import os
import json
from typing import Any, Dict, Optional

try:
    import yaml
except ImportError:
    yaml = None
try:
    import toml
except ImportError:
    toml = None


def load_config(config_path: str) -> Dict[str, Any]:
    ext = os.path.splitext(config_path)[1].lower()
    with open(config_path, "r", encoding="utf-8") as f:
        if ext in [".yaml", ".yml"]:
            if not yaml:
                raise ImportError("pyyaml is required for YAML config support")
            return yaml.safe_load(f)
        elif ext == ".json":
            return json.load(f)
        elif ext == ".toml":
            if not toml:
                raise ImportError("toml is required for TOML config support")
            return toml.load(f)
        else:
            raise ValueError(f"Unsupported config file extension: {ext}")


def get_config_from_env(
    env_var: str = "HIMALOG_CONFIG",
) -> Optional[Dict[str, Any]]:
    path = os.getenv(env_var)
    if path and os.path.isfile(path):
        return load_config(path)
    return None
