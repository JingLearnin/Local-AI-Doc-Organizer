"""CSV audit logging for every organizer decision."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


AUDIT_FIELDS = [
    "timestamp",
    "file_name",
    "source_path",
    "target_path",
    "category",
    "confidence",
    "reason",
    "action",
]


@dataclass(frozen=True)
class AuditRecord:
    """One auditable organizer decision."""

    file_name: str
    source_path: Path
    target_path: Path
    category: str
    confidence: float
    reason: str
    action: str


def append_audit_record(*, vault_path: Path, record: AuditRecord) -> Path:
    """Append one audit record to logs/audit_log.csv."""

    logs_dir = vault_path / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_path = logs_dir / "audit_log.csv"
    should_write_header = not log_path.exists()

    with log_path.open("a", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=AUDIT_FIELDS)
        if should_write_header:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "file_name": record.file_name,
                "source_path": str(record.source_path),
                "target_path": str(record.target_path),
                "category": record.category,
                "confidence": f"{record.confidence:.2f}",
                "reason": record.reason,
                "action": record.action,
            }
        )

    return log_path
