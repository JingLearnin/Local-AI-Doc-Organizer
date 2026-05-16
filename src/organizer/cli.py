"""Command line interface for Local-AI-Doc-Organizer."""

from __future__ import annotations

import argparse
from pathlib import Path

from organizer.audit_logger import AuditRecord, append_audit_record
from organizer.classifier import classify_document
from organizer.config_loader import load_rules
from organizer.mover import move_file, plan_destination
from organizer.scanner import load_documents


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""

    parser = argparse.ArgumentParser(
        prog="local-ai-doc-organizer",
        description="Organize raw local documents into a structured Obsidian-style vault.",
    )
    parser.add_argument("--vault", required=True, type=Path, help="Path to the Obsidian vault folder.")
    parser.add_argument(
        "--config",
        default=Path("config/rules.yaml"),
        type=Path,
        help="Path to YAML classification rules. Defaults to config/rules.yaml.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview actions without moving files.")
    parser.add_argument(
        "--no-audit",
        action="store_true",
        help="Do not write logs/audit_log.csv. Useful for quick local experiments.",
    )
    return parser


def run(*, vault_path: Path, config_path: Path, dry_run: bool, write_audit: bool) -> int:
    """Run one organizer pass and return a process exit code."""

    vault_path = vault_path.resolve()
    config_path = config_path.resolve()
    rules = load_rules(config_path)
    documents = load_documents(vault_path)

    if not documents:
        print(f"No files found in {vault_path / 'Unorganized'}")
        return 0

    for document in documents:
        result = classify_document(file_name=document.path.name, content=document.content, rules=rules)
        destination = plan_destination(vault_path=vault_path, source_path=document.path, category=result.category)
        action = "dry_run" if dry_run else ("moved_to_review" if result.category == "Needs_Review" else "moved")

        if not dry_run:
            move_file(document.path, destination)

        if write_audit:
            append_audit_record(
                vault_path=vault_path,
                record=AuditRecord(
                    file_name=document.path.name,
                    source_path=document.path,
                    target_path=destination,
                    category=result.category,
                    confidence=result.confidence,
                    reason=result.reason,
                    action=action,
                ),
            )

        print(
            f"{action}: {document.path.name} -> {destination.relative_to(vault_path)} "
            f"[{result.category}, confidence={result.confidence:.2f}, reason={result.reason}]"
        )

    return 0


def main() -> None:
    """CLI entry point."""

    parser = build_parser()
    args = parser.parse_args()
    raise SystemExit(
        run(
            vault_path=args.vault,
            config_path=args.config,
            dry_run=args.dry_run,
            write_audit=not args.no_audit,
        )
    )


if __name__ == "__main__":
    main()
