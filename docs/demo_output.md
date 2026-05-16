# Demo Output

This file records the expected MVP dry-run behavior for the sample vault.

## Command

```bash
PYTHONPATH=src python -m organizer.cli --vault ./sample_vault --dry-run
```

## Output

```text
dry_run: cloud_architecture.md -> Engineering/cloud_architecture.md [Engineering, confidence=0.89, reason=matched keywords: api, database, cloud, docker, python, architecture]
dry_run: resume_notes.md -> Career/resume_notes.md [Career, confidence=0.78, reason=matched keywords: resume, interview, linkedin, recruiter]
dry_run: tuition_receipt.txt -> Finance/tuition_receipt.txt [Finance, confidence=0.88, reason=matched keywords: bank, invoice, tuition, payment, receipt]
dry_run: unknown_scan.txt -> Needs_Review/unknown_scan.txt [Needs_Review, confidence=0.00, reason=no keyword match]
```

## Why This Matters

The output demonstrates the complete MVP loop: files are scanned from `Unorganized/`, classified with transparent keyword reasons, mapped to destination folders, and kept safe during preview mode.
