"""Configuration loading for organizer rules."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised by environment setup
    raise RuntimeError("PyYAML is required. Install dependencies with: pip install -r requirements.txt") from exc


class ConfigError(ValueError):
    """Raised when rules configuration is missing or invalid."""


def load_rules(config_path: Path) -> dict[str, Any]:
    """Load and validate a YAML rules file."""

    if not config_path.exists():
        raise ConfigError(f"rules file not found: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    if not isinstance(data, dict):
        raise ConfigError("rules file must contain a YAML mapping")

    if "categories" not in data or not isinstance(data["categories"], dict):
        raise ConfigError("rules file must define a 'categories' mapping")

    settings = data.setdefault("settings", {})
    if not isinstance(settings, dict):
        raise ConfigError("rules file 'settings' must be a mapping")

    settings.setdefault("default_category", "Needs_Review")
    settings.setdefault("minimum_confidence", 0.6)
    return data
