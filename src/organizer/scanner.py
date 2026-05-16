"""Vault scanning and lightweight content reading."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

SUPPORTED_TEXT_EXTENSIONS = {".md", ".txt"}


@dataclass(frozen=True)
class Document:
    """A scanned document and the text that can be read from it."""

    path: Path
    content: str


def get_unorganized_dir(vault_path: Path) -> Path:
    """Return the expected intake directory for a vault."""

    return vault_path / "Unorganized"


def scan_unorganized(vault_path: Path) -> list[Path]:
    """Return files directly under the vault's Unorganized directory."""

    unorganized_dir = get_unorganized_dir(vault_path)
    if not unorganized_dir.exists():
        raise FileNotFoundError(f"Unorganized folder not found: {unorganized_dir}")

    return sorted(path for path in unorganized_dir.iterdir() if path.is_file())


def read_supported_text(path: Path) -> str:
    """Read text for supported file types and return an empty string otherwise."""

    if path.suffix.lower() not in SUPPORTED_TEXT_EXTENSIONS:
        return ""

    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def load_documents(vault_path: Path) -> list[Document]:
    """Scan the intake folder and attach readable text content to each file."""

    return [Document(path=path, content=read_supported_text(path)) for path in scan_unorganized(vault_path)]
