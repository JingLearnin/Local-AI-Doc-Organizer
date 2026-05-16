# Local-AI-Doc-Organizer

**Local-AI-Doc-Organizer** is a local-first Python CLI tool that turns scattered technical notes and documents into a structured Obsidian-style knowledge base. It scans an intake folder, classifies files with configurable keyword rules, routes them into topic folders, and records each decision in an audit log with confidence scores and review handling.

> The goal is not to replace human judgment. The goal is to create a clear, repeatable document intake workflow that converts raw documentation into a searchable and reusable engineering knowledge base.

## Problem

Technical notes, AI conversations, course materials, resume drafts, receipts, and project documents often pile up in an unstructured folder. Over time, useful information becomes difficult to search, reuse, and build upon. This project focuses on a small but valuable automation loop: put raw files into `Unorganized/`, run the CLI, and receive a structured vault with traceable routing decisions.

## Solution

The first MVP is intentionally small. It uses a rule-based classifier rather than a complex AI agent, because the most important milestone is a complete and demonstrable engineering loop: scan, classify, route, review exceptions, and log every decision.

| Capability | MVP Behavior |
| --- | --- |
| Local-first workflow | Files are processed in a local vault folder. No cloud service is required. |
| Configurable classification | Categories and keywords live in `config/rules.yaml`. |
| Dry-run safety | `--dry-run` previews actions without moving files. |
| Review handling | Uncertain documents are routed to `Needs_Review/`. |
| Auditability | `logs/audit_log.csv` records file name, source path, target path, category, confidence, reason, timestamp, and action. |
| Supported content | The MVP reads `.md` and `.txt` files. PDF extraction is intentionally left for a later version. |

## Project Structure

```text
Local-AI-Doc-Organizer/
  config/
    rules.yaml
  docs/
    prd_and_issues.md
  sample_vault/
    Unorganized/
      cloud_architecture.md
      resume_notes.md
      tuition_receipt.txt
      unknown_scan.txt
    School/
    Career/
    Engineering/
    Finance/
    Needs_Review/
  src/
    organizer/
      __init__.py
      audit_logger.py
      classifier.py
      cli.py
      config_loader.py
      mover.py
      scanner.py
  tests/
    test_classifier.py
```

## Before and After

Before running the organizer, users drop raw files into the intake folder.

```text
sample_vault/
  Unorganized/
    cloud_architecture.md
    resume_notes.md
    tuition_receipt.txt
    unknown_scan.txt
```

After running the CLI without `--dry-run`, files are routed into structured topic folders. Low-confidence files are kept visible for manual review instead of being silently misclassified.

```text
sample_vault/
  Career/
    resume_notes.md
  Engineering/
    cloud_architecture.md
  Finance/
    tuition_receipt.txt
  Needs_Review/
    unknown_scan.txt
  logs/
    audit_log.csv
```

## Installation

Use Python 3.11 or a compatible Python 3 version. From the repository root, install the single runtime dependency.

```bash
pip install -r requirements.txt
```

If you are developing locally without installing the package, run commands with `PYTHONPATH=src`.

## Usage

The safest first command is a dry run. It previews the routing plan and writes an audit log, but it does not move files.

```bash
PYTHONPATH=src python -m organizer.cli --vault ./sample_vault --dry-run
```

A successful dry run prints output similar to the following.

```text
dry_run: cloud_architecture.md -> Engineering/cloud_architecture.md [Engineering, confidence=0.89, reason=matched keywords: api, database, cloud, docker, python, architecture]
dry_run: resume_notes.md -> Career/resume_notes.md [Career, confidence=0.78, reason=matched keywords: resume, interview, linkedin, recruiter]
dry_run: tuition_receipt.txt -> Finance/tuition_receipt.txt [Finance, confidence=0.88, reason=matched keywords: bank, invoice, tuition, payment, receipt]
dry_run: unknown_scan.txt -> Needs_Review/unknown_scan.txt [Needs_Review, confidence=0.00, reason=no keyword match]
```

When the preview looks correct, run the command without `--dry-run` to move files.

```bash
PYTHONPATH=src python -m organizer.cli --vault ./sample_vault
```

## Configuration

Rules are stored in `config/rules.yaml`. Each category defines a list of keywords, and the classifier searches both the file name and readable file content. The `minimum_confidence` setting controls when a matched file is trusted enough to move into a topic folder rather than `Needs_Review/`.

```yaml
categories:
  Engineering:
    keywords:
      - api
      - database
      - cloud
      - docker
      - system design
      - python
      - architecture

settings:
  default_category: Needs_Review
  minimum_confidence: 0.6
```

## Audit Log

Every processed file can be recorded in `sample_vault/logs/audit_log.csv`. This is the traceability layer of the project: it explains what happened, where the file came from, where it was planned or moved, and why the classifier made that decision.

| Field | Meaning |
| --- | --- |
| `timestamp` | UTC timestamp for the decision. |
| `file_name` | Name of the processed file. |
| `source_path` | Original path in `Unorganized/`. |
| `target_path` | Planned or actual destination path. |
| `category` | Selected category. |
| `confidence` | Rule-based confidence score. |
| `reason` | Human-readable classification reason. |
| `action` | `dry_run`, `moved`, or `moved_to_review`. |

## Running Tests

The MVP includes unit tests for the classifier, because classification is the core business behavior of the project.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

## Roadmap

| Version | Focus |
| --- | --- |
| v0.1 | Python CLI, rule-based classification, dry-run, safe moving, Needs Review, audit log, README demo. |
| v0.2 | PDF text extraction and richer scanner tests. |
| v0.3 | Better confidence scoring and more robust routing rules. |
| v0.4 | Optional AI fallback only when rule-based confidence is low. |

## Resume Bullet

Built a Python-based local document organizer that converts raw technical notes into a structured Obsidian-style knowledge base by scanning an intake folder, classifying files with configurable rules, routing them into topic folders, and recording each decision in an audit log with confidence scores and review handling.

## References

[1]: docs/prd_and_issues.md "MVP PRD and vertical slice plan"
