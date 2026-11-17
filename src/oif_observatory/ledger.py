"""Portable JSONL research ledger with provenance validation."""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path
from typing import Any

EVIDENCE_CLASSES = {"primary", "secondary", "reported", "community", "unverified"}
REQUIRED = ("id", "claim", "source_url", "publisher", "published_at", "observed_at", "evidence_class")


def validate_record(record: Any) -> list[str]:
    if not isinstance(record, dict):
        return ["record must be an object"]
    errors = [f"missing field: {key}" for key in REQUIRED if key not in record]
    if errors:
        return errors
    for key in ("id", "claim", "source_url", "publisher"):
        if not isinstance(record[key], str) or not record[key].strip():
            errors.append(f"{key} must be a non-empty string")
    for key in ("published_at", "observed_at"):
        try:
            date.fromisoformat(record[key])
        except (TypeError, ValueError):
            errors.append(f"{key} must be an ISO-8601 date")
    if record["evidence_class"] not in EVIDENCE_CLASSES:
        errors.append("evidence_class is not recognized")
    return errors


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"line {line_number}: invalid JSON: {exc.msg}") from exc
    return records


def validate_ledger(records: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for index, record in enumerate(records, 1):
        errors.extend(f"record {index}: {error}" for error in validate_record(record))
        if isinstance(record, dict) and isinstance(record.get("id"), str):
            if record["id"] in seen:
                errors.append(f"record {index}: duplicate id: {record['id']}")
            seen.add(record["id"])
    return errors


def write_jsonl(records: list[dict[str, Any]], path: Path) -> None:
    path.write_text("".join(json.dumps(item, sort_keys=True) + "\n" for item in records), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an OIF research JSONL ledger.")
    sub = parser.add_subparsers(dest="command", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("ledger", type=Path)
    args = parser.parse_args()
    try:
        records = load_jsonl(args.ledger)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    errors = validate_ledger(records)
    if errors:
        print("\n".join(f"ERROR: {item}" for item in errors))
        return 1
    print(f"VALID: {len(records)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
