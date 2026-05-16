"""Safe file movement and routing helpers."""

from __future__ import annotations

from pathlib import Path
from shutil import move


def unique_destination_path(destination: Path) -> Path:
    """Return a destination path that will not overwrite an existing file."""

    if not destination.exists():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    parent = destination.parent
    counter = 1

    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def plan_destination(*, vault_path: Path, source_path: Path, category: str) -> Path:
    """Plan the safe destination path for a source file and category."""

    category_dir = vault_path / category
    category_dir.mkdir(parents=True, exist_ok=True)
    return unique_destination_path(category_dir / source_path.name)


def move_file(source_path: Path, destination_path: Path) -> Path:
    """Move one file to the destination path and return the final path."""

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    move(str(source_path), str(destination_path))
    return destination_path
