# OIF Research Observatory

**An offline-first evidence ledger for tracking claims about AI, computing, security, and Open Intelligence.**

The Observatory is a small research-record toolkit. It normalizes source-backed observations into a portable JSONL ledger, detects duplicate record IDs, and applies explicit evidence labels. It does not crawl the web, authenticate sources, or convert a source's existence into proof that a claim is true.

## Implemented

- Typed research records with source URL, publisher, publication date, observation date, and evidence class.
- Required-field and date validation.
- Stable JSONL import/export.
- Duplicate-ID detection and deterministic sorting.
- CLI validation for research datasets.
- Tests covering valid records, missing provenance, dates, and duplicates.

## Quick start

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
oif-observe validate examples/sample-ledger.jsonl
```

The package uses only the Python standard library. The sample ledger is illustrative fixture material, not a claim of current events.

## Evidence classes

- `primary`: original artifact, official release, standard, filing, or direct dataset.
- `secondary`: analysis that cites primary material.
- `reported`: journalism or third-party reporting.
- `community`: public discussion or anecdotal report.
- `unverified`: source or claim not yet independently checked.

Evidence class describes source type, not truth. Store contradictions and uncertainty rather than silently choosing a preferred claim.

## Record lifecycle

Capture → validate provenance → compare with independent sources → record contradictions → assign review status → periodically re-verify. A record's observation date must not be confused with its publication date.

## Scope

This repository owns research evidence records and provenance hygiene. Shared OI resource definitions belong in [Open-Intelligence-Fabric](https://github.com/HuffmanMainNode/Open-Intelligence-Fabric). Live collection, scraping, and source-specific integrations are intentionally not included in this offline core.
